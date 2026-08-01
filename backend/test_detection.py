"""
Test language detection for ALL languages
Run: python test_detection.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from code_review.views import detect_programming_language

# Test cases for ALL languages
test_cases = [
    # C++
    ("""
#include <iostream>
using namespace std;
class Test {
public:
    virtual void test() {}
};
int main() {
    cout << "Hello" << endl;
    return 0;
}
""", 'cpp', 'C++'),

    # C
    ("""
#include <stdio.h>
#include <stdlib.h>
int main() {
    printf("Hello\\n");
    int* ptr = (int*)malloc(sizeof(int));
    free(ptr);
    return 0;
}
""", 'c', 'C'),

    # Java
    ("""
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
""", 'java', 'Java'),

    # C#
    ("""
using System;
namespace MyApp {
    class Program {
        static void Main() {
            Console.WriteLine("Hello");
        }
    }
}
""", 'csharp', 'C#'),

    # Python
    ("""
def hello():
    print("Hello")
if __name__ == "__main__":
    hello()
""", 'python', 'Python'),

    # JavaScript
    ("""
function hello() {
    console.log("Hello");
}
const x = 10;
""", 'javascript', 'JavaScript'),

    # TypeScript
    ("""
interface User {
    name: string;
    age: number;
}
type Response = { data: User[] };
""", 'typescript', 'TypeScript'),

    # Go
    ("""
package main
import "fmt"
func main() {
    fmt.Println("Hello")
}
""", 'go', 'Go'),

    # Rust
    ("""
fn main() {
    println!("Hello");
    let mut x = 5;
}
""", 'rust', 'Rust'),

    # Ruby
    ("""
def hello
    puts "Hello"
end
class Person
    attr_accessor :name
end
""", 'ruby', 'Ruby'),

    # PHP
    ("""
<?php
echo "Hello";
function hello() {
    return "Hello";
}
?>
""", 'php', 'PHP'),

    # Haskell
    ("""
module Main where
main :: IO ()
main = putStrLn "Hello"
""", 'haskell', 'Haskell'),

    # Julia
    ("""
function hello()
    println("Hello")
end
using Printf
""", 'julia', 'Julia'),

    # Swift
    ("""
import UIKit
class Hello {
    func greet() {
        print("Hello")
    }
}
""", 'swift', 'Swift'),

    # Kotlin
    ("""
fun main() {
    val name = "World"
    println("Hello $name")
}
class Person(val name: String)
""", 'kotlin', 'Kotlin'),

    # SQL
    ("""
SELECT * FROM users WHERE id = 1;
INSERT INTO users (name) VALUES ('John');
""", 'sql', 'SQL'),

    # HTML
    ("""
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body><h1>Hello</h1></body>
</html>
""", 'html', 'HTML'),

    # CSS
    ("""
body {
    color: blue;
    margin: 10px;
    padding: 20px;
}
""", 'css', 'CSS'),

    # Shell
    ("""
#!/bin/bash
echo "Hello"
export PATH=$PATH:/usr/local/bin
""", 'shell', 'Shell'),
]

print("="*60)
print("🧪 TESTING LANGUAGE DETECTION FOR ALL LANGUAGES")
print("="*60 + "\n")

passed = 0
failed = 0

for code, expected, lang_name in test_cases:
    detected = detect_programming_language(code)
    if detected == expected:
        print(f"✅ {lang_name:10} -> {detected} (CORRECT)")
        passed += 1
    else:
        print(f"❌ {lang_name:10} -> Expected: {expected}, Got: {detected}")
        failed += 1

print("\n" + "="*60)
print(f"📊 RESULTS: {passed} PASSED, {failed} FAILED")
print("="*60)

if failed == 0:
    print("🎉 ALL LANGUAGES DETECTED CORRECTLY!")
else:
    print(f"⚠️ {failed} languages failed detection")