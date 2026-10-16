CREATE DATABASE IF NOT EXISTS coursetrack_ai;
USE coursetrack_ai;

CREATE TABLE IF NOT EXISTS enquiries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    source ENUM('WhatsApp', 'Instagram', 'Facebook', 'Phone Call', 'Walk-in', 'Other') NOT NULL,
    course VARCHAR(100) NOT NULL,
    status ENUM('New', 'Contacted', 'Interested', 'Demo Attended', 'Converted', 'Lost') DEFAULT 'New',
    enquiry_date DATE NOT NULL,
    next_followup_date DATE,
    notes TEXT,
    lead_score INT DEFAULT 50,
    ai_priority VARCHAR(20) DEFAULT 'Medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);