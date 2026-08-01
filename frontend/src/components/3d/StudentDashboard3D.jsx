// frontend/src/components/student/StudentDashboard3D.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { getStats, getSubmissions } from '../../api';
import './StudentDashboard3D.css';

const StudentDashboard3D = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [stats, setStats] = useState({
    total_submissions: 0,
    completed_reviews: 0,
    pending_reviews: 0,
    total_bugs_found: 0,
    average_quality_score: 0,
    language_breakdown: {},
    recent_activity: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    console.log('📊 Fetching dashboard data...');
    setLoading(true);
    setError(null);

    try {
      // Fetch stats
      const statsResponse = await getStats();
      console.log('📊 Stats response:', statsResponse.data);
      
      let statsData = {};
      if (statsResponse.data.status === 'success') {
        statsData = statsResponse.data.data || {};
      } else {
        statsData = statsResponse.data || {};
      }
      
      console.log('📊 Stats data:', statsData);
      
      // If stats has recent_activity, use it
      let recentActivity = statsData.recent_activity || [];
      
      // If no recent activity from stats, fetch submissions directly
      if (recentActivity.length === 0) {
        try {
          const submissionsResponse = await getSubmissions();
          console.log('📋 Submissions response:', submissionsResponse.data);
          
          if (submissionsResponse.data && submissionsResponse.data.length > 0) {
            // Use submissions as recent activity
            recentActivity = submissionsResponse.data.slice(0, 5).map(sub => ({
              id: sub.id,
              title: sub.title || 'Untitled',
              status: sub.status || 'pending',
              created_at: sub.created_at,
              language: sub.language_name || sub.language?.name || 'Unknown',
              quality_score: sub.quality_score || 0,
              bug_count: sub.bug_count || 0,
              issue_count: sub.issue_count || 0,
              suggestion_count: sub.suggestion_count || 0
            }));
          }
        } catch (subErr) {
          console.log('Could not fetch submissions separately');
        }
      }
      
      setStats({
        total_submissions: statsData.total_submissions || 0,
        completed_reviews: statsData.completed_reviews || 0,
        pending_reviews: statsData.pending_reviews || 0,
        total_bugs_found: statsData.total_bugs_found || 0,
        average_quality_score: statsData.average_quality_score || 0,
        language_breakdown: statsData.language_breakdown || {},
        recent_activity: recentActivity
      });

    } catch (err) {
      console.error('❌ Failed to fetch dashboard data:', err);
      
      // Try to get submissions directly as fallback
      try {
        const submissionsResponse = await getSubmissions();
        console.log('📋 Fallback - Submissions response:', submissionsResponse.data);
        
        if (submissionsResponse.data && submissionsResponse.data.length > 0) {
          const submissions = submissionsResponse.data;
          const completed = submissions.filter(s => s.status === 'completed');
          const totalBugs = submissions.reduce((sum, s) => sum + (s.bug_count || 0), 0);
          const avgScore = completed.length > 0 
            ? completed.reduce((sum, s) => sum + (s.quality_score || 0), 0) / completed.length 
            : 0;
          
          setStats({
            total_submissions: submissions.length,
            completed_reviews: completed.length,
            pending_reviews: submissions.length - completed.length,
            total_bugs_found: totalBugs,
            average_quality_score: Math.round(avgScore),
            language_breakdown: {},
            recent_activity: submissions.slice(0, 5).map(sub => ({
              id: sub.id,
              title: sub.title || 'Untitled',
              status: sub.status || 'pending',
              created_at: sub.created_at,
              language: sub.language_name || sub.language?.name || 'Unknown',
              quality_score: sub.quality_score || 0,
              bug_count: sub.bug_count || 0,
              issue_count: sub.issue_count || 0,
              suggestion_count: sub.suggestion_count || 0
            }))
          });
        }
      } catch (fallbackErr) {
        console.error('❌ Fallback also failed:', fallbackErr);
        setError('Failed to load dashboard data. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleViewSubmission = (id) => {
    if (id) {
      navigate(`/submission/${id}`);
    }
  };

  const handleNewSubmission = () => {
    navigate('/submit');
  };

  const handleViewAllSubmissions = () => {
    navigate('/submissions');
  };

  const handleViewCompletedReviews = () => {
    navigate('/submissions?status=completed');
  };

  const handleViewBugs = () => {
    navigate('/submissions?filter=bugs');
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <p>❌ {error}</p>
        <button onClick={fetchDashboardData} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="student-dashboard-3d">
      {/* Welcome Section */}
      <div className="welcome-section">
        <h1>Welcome back, {user?.username || 'Student'}!</h1>
        <p className="user-role">
          Student • {user?.college || 'Arunai engineering college'}
        </p>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card" onClick={handleViewAllSubmissions}>
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>{stats.total_submissions}</h3>
            <p>Total Submissions</p>
          </div>
          <span className="stat-hint">Click to view all submissions</span>
        </div>

        <div className="stat-card" onClick={handleViewCompletedReviews}>
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>{stats.completed_reviews}</h3>
            <p>Completed Reviews</p>
          </div>
          <span className="stat-hint">Click to view completed reviews</span>
        </div>

        <div className="stat-card" onClick={handleViewBugs}>
          <div className="stat-icon">🐛</div>
          <div className="stat-content">
            <h3>{stats.total_bugs_found}</h3>
            <p>Bugs Found</p>
          </div>
          <span className="stat-hint">Click to view all bugs</span>
        </div>

        <div className="stat-card quality-score">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <h3>{stats.average_quality_score}%</h3>
            <p>Quality Score</p>
          </div>
          <span className="stat-hint">Average quality score</span>
        </div>
      </div>

      {/* Recent Submissions */}
      <div className="recent-section">
        <div className="section-header">
          <h2>Recent Submissions</h2>
          <button className="view-all-btn" onClick={handleViewAllSubmissions}>
            View All →
          </button>
        </div>

        {stats.recent_activity && stats.recent_activity.length > 0 ? (
          <div className="recent-list">
            {stats.recent_activity.map((submission, index) => (
              <div 
                key={submission.id || index} 
                className="recent-item"
                onClick={() => handleViewSubmission(submission.id)}
              >
                <div className="recent-info">
                  <span className="recent-title">{submission.title || 'Untitled'}</span>
                  <span className="recent-language">{submission.language || 'Unknown'}</span>
                </div>
                <div className="recent-stats">
                  <span className={`recent-status ${submission.status || 'pending'}`}>
                    {submission.status === 'completed' ? '✅' : '⏳'} {submission.status || 'pending'}
                  </span>
                  {submission.quality_score > 0 && (
                    <span className="recent-score">{submission.quality_score}%</span>
                  )}
                  <span className="recent-date">
                    {submission.created_at ? new Date(submission.created_at).toLocaleDateString() : 'N/A'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No submissions yet. Start your first code review!</p>
            <button className="start-review-btn" onClick={handleNewSubmission}>
              Submit Your First Code
            </button>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h3>Quick Actions</h3>
        <div className="actions-grid">
          <button className="action-btn primary" onClick={handleNewSubmission}>
            ✏️ New Submission
          </button>
          <button className="action-btn secondary" onClick={() => navigate('/history')}>
            📜 Review History
          </button>
          <button className="action-btn secondary" onClick={() => navigate('/profile')}>
            👤 My Profile
          </button>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard3D;