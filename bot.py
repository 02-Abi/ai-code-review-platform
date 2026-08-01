"""
Telegram Payment Bot - Production Ready Version
"""
import os
import json
import logging
import sqlite3
import threading
import random
import string
import hashlib
import hmac
import time
import asyncio
import datetime
from typing import Dict, Optional, List, Any, Tuple, Union
from dataclasses import dataclass, asdict
from contextlib import contextmanager
from functools import wraps

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
import pytz

# ============================================================
# CONFIGURATION
# ============================================================

class Config:
    """Application configuration"""
    
    # Environment variables
    API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not API_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
    
    ADMIN_IDS = [int(x.strip()) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip()]
    
    # Constants
    DATABASE_FILE = os.getenv('DATABASE_FILE', 'bot_data.db')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    RATE_LIMIT_SECONDS = int(os.getenv('RATE_LIMIT_SECONDS', 5))
    MAX_TRANSACTION_AMOUNT = float(os.getenv('MAX_TRANSACTION_AMOUNT', 10000))
    GIFT_CODE_LENGTH = int(os.getenv('GIFT_CODE_LENGTH', 10))
    GIFT_CODE_EXPIRY_DAYS = int(os.getenv('GIFT_CODE_EXPIRY_DAYS', 7))
    MAX_BOOKINGS_PER_GUEST = int(os.getenv('MAX_BOOKINGS_PER_GUEST', 3))
    REQUEST_TIMEOUT = 30

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL),
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def rate_limit(limit_seconds: int = Config.RATE_LIMIT_SECONDS):
    """Rate limiting decorator"""
    user_last_action = {}
    
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = str(update.effective_user.id)
            current_time = time.time()
            
            if user_id in user_last_action:
                if current_time - user_last_action[user_id] < limit_seconds:
                    await update.message.reply_text(
                        f"⏳ Please wait {limit_seconds} seconds between actions!"
                    )
                    return
            
            user_last_action[user_id] = current_time
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator

def admin_required(func):
    """Admin authentication decorator"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in Config.ADMIN_IDS:
            await update.message.reply_text("⛔ You are not authorized to access this command!")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def generate_random_code(length: int = Config.GIFT_CODE_LENGTH) -> str:
    """Generate a random alphanumeric code"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    if not text:
        return ""
    # Remove any non-alphanumeric except spaces
    return ''.join(c for c in text if c.isalnum() or c.isspace())

# ============================================================
# DATABASE LAYER
# ============================================================

@dataclass
class User:
    """User data model"""
    user_id: str
    username: str
    balance: float
    registered_at: str
    is_active: bool = True
    
@dataclass
class Transaction:
    """Transaction data model"""
    id: int
    user_id: str
    amount: float
    type: str
    description: str
    created_at: str
    
@dataclass
class GiftCode:
    """Gift code data model"""
    code: str
    amount: float
    generated_by: str
    expiry: str
    used: bool = False

class Database:
    """Database layer with connection pooling and atomic operations"""
    
    def __init__(self, db_file: str = Config.DATABASE_FILE):
        self.db_file = db_file
        self._lock = threading.RLock()
        self._init_database()
        logger.info(f"Database initialized: {db_file}")
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """Initialize database schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT,
                    balance REAL DEFAULT 0,
                    registered_at TEXT,
                    is_active INTEGER DEFAULT 1,
                    last_active TEXT
                )
            ''')
            
            # Transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    amount REAL,
                    type TEXT,
                    description TEXT,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # Gift codes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gift_codes (
                    code TEXT PRIMARY KEY,
                    amount REAL,
                    generated_by TEXT,
                    expiry TEXT,
                    used INTEGER DEFAULT 0,
                    used_by TEXT,
                    used_at TEXT,
                    FOREIGN KEY (generated_by) REFERENCES users(user_id)
                )
            ''')
            
            # Referrals table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id TEXT,
                    referred_id TEXT,
                    created_at TEXT,
                    status TEXT,
                    FOREIGN KEY (referrer_id) REFERENCES users(user_id),
                    FOREIGN KEY (referred_id) REFERENCES users(user_id)
                )
            ''')
            
            # Indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON users(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_trans_user_id ON transactions(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_trans_created ON transactions(created_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_gift_code ON gift_codes(code)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_gift_expiry ON gift_codes(expiry)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_ref_referrer ON referrals(referrer_id)')
            
            conn.commit()
            logger.info("Database schema initialized")
    
    # ===== USER OPERATIONS =====
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, username, balance, registered_at, is_active
                FROM users WHERE user_id = ?
            ''', (user_id,))
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row['user_id'],
                    username=row['username'],
                    balance=row['balance'],
                    registered_at=row['registered_at'],
                    is_active=bool(row['is_active'])
                )
            return None
    
    def create_user(self, user_id: str, username: str) -> bool:
        """Create a new user"""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                now = datetime.datetime.now(pytz.UTC).isoformat()
                cursor.execute('''
                    INSERT INTO users (user_id, username, registered_at, last_active)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, username, now, now))
                conn.commit()
                logger.info(f"User created: {user_id} ({username})")
                return True
            except sqlite3.IntegrityError:
                logger.warning(f"User already exists: {user_id}")
                return False
    
    def update_user_balance(self, user_id: str, amount: float) -> bool:
        """Update user balance atomically"""
        with self._lock:
            with self._get_connection() as conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE users 
                        SET balance = balance + ? 
                        WHERE user_id = ? AND balance + ? >= 0
                    ''', (amount, user_id, amount))
                    
                    if cursor.rowcount == 0:
                        return False
                    
                    cursor.execute('''
                        UPDATE users SET last_active = ? WHERE user_id = ?
                    ''', (datetime.datetime.now(pytz.UTC).isoformat(), user_id))
                    
                    conn.commit()
                    logger.info(f"Balance updated for {user_id}: {amount}")
                    return True
                except Exception as e:
                    conn.rollback()
                    logger.error(f"Failed to update balance: {e}")
                    return False
    
    def transfer_balance(self, from_user_id: str, to_user_id: str, amount: float) -> Tuple[bool, str]:
        """Transfer balance between users atomically"""
        with self._lock:
            with self._get_connection() as conn:
                try:
                    cursor = conn.cursor()
                    
                    # Check sender balance
                    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (from_user_id,))
                    row = cursor.fetchone()
                    if not row:
                        return False, "Sender not found"
                    if row['balance'] < amount:
                        return False, "Insufficient balance"
                    
                    # Check receiver exists
                    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (to_user_id,))
                    if not cursor.fetchone():
                        return False, "Recipient not found"
                    
                    # Perform transfer
                    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, from_user_id))
                    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, to_user_id))
                    
                    # Record transactions
                    now = datetime.datetime.now(pytz.UTC).isoformat()
                    cursor.execute('''
                        INSERT INTO transactions (user_id, amount, type, description, created_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (from_user_id, -amount, 'transfer', f'Transfer to {to_user_id}', now))
                    
                    cursor.execute('''
                        INSERT INTO transactions (user_id, amount, type, description, created_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (to_user_id, amount, 'transfer', f'Transfer from {from_user_id}', now))
                    
                    conn.commit()
                    logger.info(f"Transfer successful: {from_user_id} -> {to_user_id} (${amount})")
                    return True, "Transfer successful"
                    
                except Exception as e:
                    conn.rollback()
                    logger.error(f"Transfer failed: {e}")
                    return False, "Transfer failed"
    
    # ===== TRANSACTION OPERATIONS =====
    
    def add_transaction(self, user_id: str, amount: float, type: str, description: str) -> bool:
        """Add a transaction record"""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions (user_id, amount, type, description, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, amount, type, description, datetime.datetime.now(pytz.UTC).isoformat()))
                conn.commit()
                return True
            except Exception as e:
                logger.error(f"Failed to add transaction: {e}")
                return False
    
    def get_transactions(self, user_id: str, limit: int = 50) -> List[Transaction]:
        """Get user transaction history"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, user_id, amount, type, description, created_at
                FROM transactions
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            return [
                Transaction(
                    id=row['id'],
                    user_id=row['user_id'],
                    amount=row['amount'],
                    type=row['type'],
                    description=row['description'],
                    created_at=row['created_at']
                )
                for row in rows
            ]
    
    # ===== GIFT CODE OPERATIONS =====
    
    def generate_gift_code(self, user_id: str, amount: float) -> Optional[str]:
        """Generate a new gift code"""
        with self._lock:
            with self._get_connection() as conn:
                try:
                    cursor = conn.cursor()
                    
                    # Generate unique code
                    code = generate_random_code()
                    while True:
                        cursor.execute('SELECT code FROM gift_codes WHERE code = ?', (code,))
                        if not cursor.fetchone():
                            break
                        code = generate_random_code()
                    
                    # Store gift code
                    expiry = datetime.datetime.now(pytz.UTC) + datetime.timedelta(days=Config.GIFT_CODE_EXPIRY_DAYS)
                    cursor.execute('''
                        INSERT INTO gift_codes (code, amount, generated_by, expiry)
                        VALUES (?, ?, ?, ?)
                    ''', (code, amount, user_id, expiry.isoformat()))
                    
                    conn.commit()
                    logger.info(f"Gift code generated: {code} by {user_id}")
                    return code
                    
                except Exception as e:
                    conn.rollback()
                    logger.error(f"Failed to generate gift code: {e}")
                    return None
    
    def redeem_gift_code(self, code: str, user_id: str) -> Tuple[bool, str, float]:
        """Redeem a gift code"""
        with self._lock:
            with self._get_connection() as conn:
                try:
                    cursor = conn.cursor()
                    
                    # Get gift code
                    cursor.execute('''
                        SELECT amount, generated_by, expiry, used FROM gift_codes WHERE code = ?
                    ''', (code,))
                    row = cursor.fetchone()
                    
                    if not row:
                        return False, "Invalid gift code", 0.0
                    
                    if row['used']:
                        return False, "Gift code already used", 0.0
                    
                    # Check expiry
                    expiry = datetime.datetime.fromisoformat(row['expiry'])
                    if datetime.datetime.now(pytz.UTC) > expiry:
                        return False, "Gift code has expired", 0.0
                    
                    # Redeem
                    amount = row['amount']
                    cursor.execute('UPDATE gift_codes SET used = 1, used_by = ?, used_at = ? WHERE code = ?',
                                 (user_id, datetime.datetime.now(pytz.UTC).isoformat(), code))
                    
                    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
                    
                    # Record transaction
                    cursor.execute('''
                        INSERT INTO transactions (user_id, amount, type, description, created_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (user_id, amount, 'gift_code', f'Redeemed gift code: {code}', datetime.datetime.now(pytz.UTC).isoformat()))
                    
                    conn.commit()
                    logger.info(f"Gift code redeemed: {code} by {user_id}")
                    return True, "Gift code redeemed successfully", amount
                    
                except Exception as e:
                    conn.rollback()
                    logger.error(f"Failed to redeem gift code: {e}")
                    return False, "Failed to redeem gift code", 0.0
    
    def get_all_users(self) -> List[User]:
        """Get all users (admin only)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user_id, username, balance, registered_at, is_active FROM users ORDER BY registered_at DESC')
            rows = cursor.fetchall()
            return [
                User(
                    user_id=row['user_id'],
                    username=row['username'],
                    balance=row['balance'],
                    registered_at=row['registered_at'],
                    is_active=bool(row['is_active'])
                )
                for row in rows
            ]
    
    def get_total_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM users')
            total_users = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
            active_users = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(balance) FROM users')
            total_balance = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT COUNT(*) FROM transactions')
            total_transactions = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(amount) FROM transactions WHERE type = "deposit"')
            total_deposits = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT COUNT(*) FROM gift_codes WHERE used = 0')
            active_gift_codes = cursor.fetchone()[0]
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'total_balance': total_balance,
                'total_transactions': total_transactions,
                'total_deposits': total_deposits,
                'active_gift_codes': active_gift_codes
            }

# ============================================================
# TELEGRAM BOT HANDLERS
# ============================================================

class BotHandlers:
    """Telegram bot command and callback handlers"""
    
    def __init__(self, db: Database):
        self.db = db
    
    # ===== COMMAND HANDLERS =====
    
    @rate_limit()
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        try:
            user_id = str(update.effective_user.id)
            username = update.effective_user.username or 'Unknown'
            
            user = self.db.get_user(user_id)
            if not user:
                self.db.create_user(user_id, username)
                await update.message.reply_text(
                    "🎉 **Welcome to the Payment Bot!**\n\n"
                    "Your account has been successfully created.\n"
                    "Use the /menu command to explore all features.\n\n"
                    "💡 **Available Commands:**\n"
                    "/menu - Show main menu\n"
                    "/balance - Check your balance\n"
                    "/history - View transaction history\n"
                    "/help - Show help message",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    f"👋 **Welcome Back, {username}!**\n\n"
                    "Use the /menu command to access all features.\n\n"
                    f"💰 Current Balance: **${user.balance:.2f}**",
                    parse_mode='Markdown'
                )
            
            logger.info(f"User started bot: {user_id} ({username})")
            
        except Exception as e:
            logger.error(f"Error in start: {e}")
            await update.message.reply_text("⚠️ An error occurred. Please try again later.")
    
    @rate_limit()
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        try:
            help_text = """
📚 **Bot Commands & Features**

**General Commands:**
/start - Start the bot
/menu - Show main menu
/balance - Check your balance
/history - View transaction history
/help - Show this help message

**Features:**
💰 Add Money - Add funds to your wallet
📤 Transfer Money - Send money to other users
🎫 Gift Codes - Generate and redeem gift codes
📊 Transaction History - View all transactions
🤝 Referral System - Earn rewards for referrals

**Security:**
🔐 All transactions are secured and logged
⏳ Rate limiting prevents spam
🛡️ Input validation on all commands

**Need help?** Contact the admin.
"""
            await update.message.reply_text(help_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in help: {e}")
            await update.message.reply_text("⚠️ An error occurred.")
    
    @rate_limit()
    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /balance command"""
        try:
            user_id = str(update.effective_user.id)
            user = self.db.get_user(user_id)
            
            if not user:
                await update.message.reply_text("❌ User not found. Please use /start to register.")
                return
            
            await update.message.reply_text(
                f"💰 **Your Balance**\n\n"
                f"Balance: **${user.balance:.2f}**\n\n"
                f"User: @{user.username or 'Unknown'}\n"
                f"Registered: {user.registered_at[:10]}\n"
                f"Active: {'✅' if user.is_active else '❌'}",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in balance: {e}")
            await update.message.reply_text("⚠️ An error occurred.")
    
    @rate_limit()
    async def history(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /history command"""
        try:
            user_id = str(update.effective_user.id)
            transactions = self.db.get_transactions(user_id, 20)
            
            if not transactions:
                await update.message.reply_text("📊 No transactions found.")
                return
            
            history_text = "📊 **Transaction History**\n\n"
            for t in transactions[:10]:
                sign = "+" if t.amount > 0 else ""
                history_text += f"• {t.created_at[:10]}: {sign}${t.amount:.2f} - {t.description}\n"
            
            if len(transactions) > 10:
                history_text += f"\n... and {len(transactions) - 10} more transactions."
            
            await update.message.reply_text(history_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in history: {e}")
            await update.message.reply_text("⚠️ An error occurred.")
    
    # ===== CALLBACK HANDLERS =====
    
    async def main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show main menu"""
        try:
            keyboard = [
                [InlineKeyboardButton("💰 Balance", callback_data='balance')],
                [InlineKeyboardButton("📤 Add Money", callback_data='add_money')],
                [InlineKeyboardButton("📨 Transfer", callback_data='transfer')],
                [InlineKeyboardButton("🎫 Gift Code", callback_data='gift_code')],
                [InlineKeyboardButton("📊 History", callback_data='history')],
                [InlineKeyboardButton("📝 Help", callback_data='help')],
            ]
            
            user_id = update.effective_user.id
            if user_id in Config.ADMIN_IDS:
                keyboard.append([InlineKeyboardButton("🔐 Admin Panel", callback_data='admin')])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    "🌟 **Main Menu**\n\nSelect an option below:",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    "🌟 **Main Menu**\n\nSelect an option below:",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logger.error(f"Error in main_menu: {e}")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle button callbacks"""
        try:
            query = update.callback_query
            await query.answer()
            
            user_id = str(update.effective_user.id)
            data = query.data
            
            if data == 'balance':
                await self.balance_callback(update, context)
            elif data == 'add_money':
                await self.add_money_callback(update, context)
            elif data == 'transfer':
                await self.transfer_callback(update, context)
            elif data == 'gift_code':
                await self.gift_code_callback(update, context)
            elif data == 'history':
                await self.history_callback(update, context)
            elif data == 'help':
                await self.help_callback(update, context)
            elif data == 'admin' and update.effective_user.id in Config.ADMIN_IDS:
                await self.admin_callback(update, context)
            elif data.startswith('add_amount_'):
                amount = float(data.split('_')[2])
                await self.process_add_money(update, context, amount)
            elif data.startswith('generate_gift_'):
                amount = float(data.split('_')[2])
                await self.generate_gift_callback(update, context, amount)
            elif data == 'back_to_menu':
                await self.main_menu(update, context)
            elif data == 'refresh_balance':
                await self.balance_callback(update, context)
                
        except Exception as e:
            logger.error(f"Error in button_callback: {e}")
    
    # ===== SPECIFIC CALLBACKS =====
    
    async def balance_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show balance from callback"""
        try:
            user_id = str(update.effective_user.id)
            user = self.db.get_user(user_id)
            
            if not user:
                await update.callback_query.edit_message_text("❌ User not found.")
                return
            
            keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data='refresh_balance')],
                       [InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
            
            await update.callback_query.edit_message_text(
                f"💰 **Your Balance**\n\n"
                f"Balance: **${user.balance:.2f}**\n\n"
                f"User: @{user.username or 'Unknown'}\n"
                f"Registered: {user.registered_at[:10]}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in balance_callback: {e}")
    
    async def add_money_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show add money options"""
        try:
            keyboard = [
                [InlineKeyboardButton("$10", callback_data='add_amount_10'),
                 InlineKeyboardButton("$50", callback_data='add_amount_50')],
                [InlineKeyboardButton("$100", callback_data='add_amount_100'),
                 InlineKeyboardButton("$500", callback_data='add_amount_500')],
                [InlineKeyboardButton("$1000", callback_data='add_amount_1000')],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]
            ]
            
            await update.callback_query.edit_message_text(
                "💰 **Add Money**\n\n"
                "Select an amount to add to your wallet:\n\n"
                f"⚠️ Maximum deposit: **${Config.MAX_TRANSACTION_AMOUNT:.2f}**",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in add_money_callback: {e}")
    
    async def process_add_money(self, update: Update, context: ContextTypes.DEFAULT_TYPE, amount: float) -> None:
        """Process add money request"""
        try:
            user_id = str(update.effective_user.id)
            
            if amount <= 0:
                await update.callback_query.edit_message_text("❌ Amount must be positive!")
                return
            
            if amount > Config.MAX_TRANSACTION_AMOUNT:
                await update.callback_query.edit_message_text(
                    f"❌ Maximum deposit is ${Config.MAX_TRANSACTION_AMOUNT:.2f}!"
                )
                return
            
            # Update balance
            if self.db.update_user_balance(user_id, amount):
                self.db.add_transaction(user_id, amount, 'deposit', f'Deposited ${amount:.2f}')
                
                user = self.db.get_user(user_id)
                keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
                
                await update.callback_query.edit_message_text(
                    f"✅ **Deposit Successful!**\n\n"
                    f"Added: **${amount:.2f}**\n"
                    f"New Balance: **${user.balance:.2f}**",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode='Markdown'
                )
                logger.info(f"Deposit successful: {user_id} - ${amount}")
            else:
                await update.callback_query.edit_message_text("❌ Failed to process deposit. Please try again.")
                
        except Exception as e:
            logger.error(f"Error in process_add_money: {e}")
            await update.callback_query.edit_message_text("⚠️ An error occurred.")
    
    async def transfer_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle transfer callback"""
        try:
            await update.callback_query.edit_message_text(
                "📨 **Transfer Money**\n\n"
                "Use the command:\n"
                "`/transfer @username amount`\n\n"
                "Example:\n"
                "`/transfer @john 50`\n\n"
                "This will send $50 to @john.\n\n"
                "⚠️ You can only send money to registered users.",
                parse_mode='Markdown'
            )
            context.user_data['transfer_mode'] = True
            
        except Exception as e:
            logger.error(f"Error in transfer_callback: {e}")
    
    async def gift_code_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle gift code callback"""
        try:
            keyboard = [
                [InlineKeyboardButton("🎫 Generate Gift Code", callback_data='generate_gift_10')],
                [InlineKeyboardButton("🔄 Redeem Gift Code", callback_data='redeem_gift')],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]
            ]
            
            await update.callback_query.edit_message_text(
                "🎫 **Gift Code System**\n\n"
                "**Generate** - Create a gift code to share with friends\n"
                "**Redeem** - Use a gift code to add funds\n\n"
                "💡 Gift codes expire in 7 days.\n"
                "💡 Each code can only be used once.",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in gift_code_callback: {e}")
    
    async def generate_gift_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE, amount: float) -> None:
        """Generate gift code"""
        try:
            user_id = str(update.effective_user.id)
            
            # Check if user has enough balance (optional)
            user = self.db.get_user(user_id)
            if not user:
                await update.callback_query.edit_message_text("❌ User not found.")
                return
            
            if user.balance < amount:
                await update.callback_query.edit_message_text(
                    f"❌ Insufficient balance to generate ${amount:.2f} gift code.\n"
                    f"Your balance: ${user.balance:.2f}"
                )
                return
            
            # Deduct from balance
            if not self.db.update_user_balance(user_id, -amount):
                await update.callback_query.edit_message_text("❌ Failed to generate gift code.")
                return
            
            # Generate gift code
            code = self.db.generate_gift_code(user_id, amount)
            if not code:
                # Refund if failed
                self.db.update_user_balance(user_id, amount)
                await update.callback_query.edit_message_text("❌ Failed to generate gift code.")
                return
            
            self.db.add_transaction(user_id, -amount, 'gift_code_gen', f'Generated gift code: {code}')
            
            keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
            
            await update.callback_query.edit_message_text(
                f"🎫 **Gift Code Generated!**\n\n"
                f"Code: `{code}`\n"
                f"Amount: **${amount:.2f}**\n"
                f"Expires: {Config.GIFT_CODE_EXPIRY_DAYS} days\n\n"
                f"Share this code with friends!\n\n"
                f"💰 Your new balance: **${self.db.get_user(user_id).balance:.2f}**",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in generate_gift_callback: {e}")
    
    async def history_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show transaction history"""
        try:
            user_id = str(update.effective_user.id)
            transactions = self.db.get_transactions(user_id, 20)
            
            if not transactions:
                keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
                await update.callback_query.edit_message_text(
                    "📊 No transactions found.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return
            
            history_text = "📊 **Transaction History**\n\n"
            for t in transactions[:10]:
                sign = "+" if t.amount > 0 else ""
                emoji = "💰" if t.amount > 0 else "📤"
                history_text += f"{emoji} {t.created_at[:10]}: {sign}${t.amount:.2f} - {t.description}\n"
            
            if len(transactions) > 10:
                history_text += f"\n... and {len(transactions) - 10} more transactions."
            
            keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data='refresh_balance')],
                       [InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
            
            await update.callback_query.edit_message_text(
                history_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in history_callback: {e}")
    
    async def help_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show help"""
        try:
            await update.callback_query.edit_message_text(
                "📚 **Help & Support**\n\n"
                "**Commands:**\n"
                "/start - Start the bot\n"
                "/menu - Show main menu\n"
                "/balance - Check balance\n"
                "/history - View transactions\n"
                "/help - Show help\n\n"
                "**Features:**\n"
                "💰 Add Money - Instantly add funds\n"
                "📤 Transfer - Send money to others\n"
                "🎫 Gift Codes - Generate and redeem\n"
                "📊 History - Track all transactions\n\n"
                "**Need help?** Contact the admin.",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in help_callback: {e}")
    
    # ===== ADMIN HANDLERS =====
    
    @admin_required
    async def admin_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Admin dashboard"""
        try:
            stats = self.db.get_total_stats()
            
            keyboard = [
                [InlineKeyboardButton("👥 View Users", callback_data='admin_users')],
                [InlineKeyboardButton("💰 Total Revenue", callback_data='admin_revenue')],
                [InlineKeyboardButton("📊 System Stats", callback_data='admin_stats')],
                [InlineKeyboardButton("🎫 Gift Codes", callback_data='admin_gift_codes')],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]
            ]
            
            await update.callback_query.edit_message_text(
                f"🔐 **Admin Dashboard**\n\n"
                f"📊 **System Statistics:**\n"
                f"• Total Users: **{stats['total_users']}**\n"
                f"• Active Users: **{stats['active_users']}**\n"
                f"• Total Balance: **${stats['total_balance']:.2f}**\n"
                f"• Total Transactions: **{stats['total_transactions']}**\n"
                f"• Total Deposits: **${stats['total_deposits']:.2f}**\n"
                f"• Active Gift Codes: **{stats['active_gift_codes']}**",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in admin_callback: {e}")
    
    # ===== MESSAGE HANDLERS =====
    
    async def handle_transfer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle transfer command"""
        try:
            text = update.message.text
            parts = text.split()
            
            if len(parts) != 3:
                await update.message.reply_text(
                    "❌ Invalid format!\n"
                    "Use: `/transfer @username amount`\n"
                    "Example: `/transfer @john 50`"
                )
                return
            
            # Parse recipient
            recipient = parts[1]
            if recipient.startswith('@'):
                recipient = recipient[1:]
            
            # Parse amount
            try:
                amount = float(parts[2])
            except ValueError:
                await update.message.reply_text("❌ Invalid amount! Please enter a number.")
                return
            
            # Validate
            if amount <= 0:
                await update.message.reply_text("❌ Amount must be positive!")
                return
            
            if amount > Config.MAX_TRANSACTION_AMOUNT:
                await update.message.reply_text(f"❌ Maximum transfer amount is ${Config.MAX_TRANSACTION_AMOUNT:.2f}!")
                return
            
            from_user_id = str(update.effective_user.id)
            
            # Find recipient
            all_users = self.db.get_all_users()
            to_user = None
            for user in all_users:
                if user.username.lower() == recipient.lower():
                    to_user = user
                    break
            
            if not to_user:
                await update.message.reply_text(f"❌ User @{recipient} not found!")
                return
            
            if to_user.user_id == from_user_id:
                await update.message.reply_text("❌ Cannot transfer to yourself!")
                return
            
            # Process transfer
            success, message = self.db.transfer_balance(from_user_id, to_user_id, amount)
            
            if success:
                await update.message.reply_text(
                    f"✅ **Transfer Successful!**\n\n"
                    f"Sent: **${amount:.2f}** to @{recipient}\n"
                    f"New Balance: **${self.db.get_user(from_user_id).balance:.2f}**",
                    parse_mode='Markdown'
                )
                
                # Notify recipient
                try:
                    await context.bot.send_message(
                        chat_id=int(to_user_id),
                        text=f"📨 **Money Received!**\n\n"
                             f"You received **${amount:.2f}** from @{update.effective_user.username}\n"
                             f"New Balance: **${to_user.balance:.2f}**",
                        parse_mode='Markdown'
                    )
                except Exception as e:
                    logger.warning(f"Could not notify recipient: {e}")
            else:
                await update.message.reply_text(f"❌ {message}")
                
        except Exception as e:
            logger.error(f"Error in handle_transfer: {e}")
            await update.message.reply_text("⚠️ An error occurred during transfer.")
    
    async def handle_redeem_gift(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle gift code redemption"""
        try:
            text = update.message.text
            parts = text.split()
            
            if len(parts) != 2:
                await update.message.reply_text(
                    "❌ Invalid format!\n"
                    "Use: `/redeem GIFT_CODE`"
                )
                return
            
            code = parts[1].strip().upper()
            
            # Validate code
            if len(code) != Config.GIFT_CODE_LENGTH or not code.isalnum():
                await update.message.reply_text("❌ Invalid gift code format!")
                return
            
            user_id = str(update.effective_user.id)
            success, message, amount = self.db.redeem_gift_code(code, user_id)
            
            if success:
                await update.message.reply_text(
                    f"✅ **Gift Code Redeemed!**\n\n"
                    f"Amount: **${amount:.2f}**\n"
                    f"New Balance: **${self.db.get_user(user_id).balance:.2f}**",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(f"❌ {message}")
                
        except Exception as e:
            logger.error(f"Error in handle_redeem_gift: {e}")
            await update.message.reply_text("⚠️ An error occurred while redeeming.")

# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    """Start the bot application"""
    try:
        logger.info("🚀 Starting Telegram Payment Bot...")
        
        # Initialize database
        db = Database()
        logger.info("✅ Database initialized")
        
        # Initialize handlers
        handlers = BotHandlers(db)
        logger.info("✅ Handlers initialized")
        
        # Create application
        application = Application.builder().token(Config.API_TOKEN).build()
        logger.info("✅ Application created")
        
        # Register command handlers
        application.add_handler(CommandHandler("start", handlers.start))
        application.add_handler(CommandHandler("menu", handlers.main_menu))
        application.add_handler(CommandHandler("balance", handlers.balance))
        application.add_handler(CommandHandler("history", handlers.history))
        application.add_handler(CommandHandler("help", handlers.help_command))
        application.add_handler(CommandHandler("transfer", handlers.handle_transfer))
        application.add_handler(CommandHandler("redeem", handlers.handle_redeem_gift))
        
        # Register callback handler
        application.add_handler(CallbackQueryHandler(handlers.button_callback))
        
        # Register message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_transfer))
        
        # Start bot
        logger.info("✅ Bot is running...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        raise

if __name__ == '__main__':
    main()