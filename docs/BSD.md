# Business System Design (BSD)
## Portfolio Management System

**Project Name:** Taskmaster Portfolio  
**Version:** 1.0  
**Date:** December 13, 2025  
**Author:** Fitrah

---

## 1. Executive Summary

Portfolio Management System adalah aplikasi web modern yang dirancang untuk menampilkan portfolio profesional, skills, pengalaman kerja, dan project yang telah dikerjakan. Sistem ini memungkinkan admin untuk mengelola konten secara dinamis melalui dashboard admin yang user-friendly.

### 1.1 Business Goals
- Menyediakan platform untuk showcase portfolio profesional
- Memudahkan proses update konten portfolio tanpa coding
- Meningkatkan profesionalisme dalam presentasi karya
- Memfasilitasi komunikasi dengan potential clients/employers

### 1.2 Target Users
1. **Visitors/Public**: Calon client, recruiter, atau siapapun yang ingin melihat portfolio
2. **Admin**: Pemilik portfolio yang mengelola konten

---

## 2. Business Requirements

### 2.1 Functional Requirements

#### FR-01: Portfolio Display
- **Priority:** High
- **Description:** Sistem harus dapat menampilkan portfolio projects dengan informasi detail
- **Acceptance Criteria:**
  - Menampilkan list projects dengan thumbnail
  - Filtering berdasarkan kategori
  - Search functionality
  - Sorting options (latest, most viewed, most liked)
  - Pagination untuk performa optimal

#### FR-02: Skills Management
- **Priority:** High
- **Description:** Menampilkan skills dengan level proficiency
- **Acceptance Criteria:**
  - Visual skill bars menunjukkan level keahlian
  - Categorization (Backend, Frontend, Design, etc.)
  - Icon representation untuk setiap skill

#### FR-03: Experience Timeline
- **Priority:** High
- **Description:** Menampilkan work experience dalam bentuk timeline
- **Acceptance Criteria:**
  - Chronological order (terbaru di atas)
  - Indicator untuk current position
  - Detail informasi (company, location, duration, description)

#### FR-04: Blog/Articles
- **Priority:** Medium
- **Description:** Platform untuk sharing knowledge melalui artikel
- **Acceptance Criteria:**
  - List articles dengan cover image
  - View count tracking
  - Tags categorization
  - Responsive design untuk reading experience

#### FR-05: Contact Form
- **Priority:** High
- **Description:** Memfasilitasi komunikasi dari visitors
- **Acceptance Criteria:**
  - Form validation
  - Email notification (optional)
  - Message storage in database
  - Success confirmation

#### FR-06: Admin Authentication
- **Priority:** High
- **Description:** Secure login system untuk admin
- **Acceptance Criteria:**
  - Username/password authentication
  - JWT token-based session
  - Session timeout (24 hours)
  - Secure password storage (hashed)

#### FR-07: Content Management
- **Priority:** High
- **Description:** CRUD operations untuk semua konten
- **Acceptance Criteria:**
  - Add/Edit/Delete projects
  - Add/Delete skills
  - Add/Delete experiences
  - Add articles
  - Manage messages
  - Image upload functionality

#### FR-08: Analytics Dashboard
- **Priority:** Medium
- **Description:** Dashboard untuk melihat statistics
- **Acceptance Criteria:**
  - Total projects, views, likes
  - Recent projects
  - Unread messages count
  - Popular projects

### 2.2 Non-Functional Requirements

#### NFR-01: Performance
- Page load time < 3 seconds
- API response time < 500ms
- Support concurrent users (minimum 100)

#### NFR-02: Usability
- Responsive design (mobile, tablet, desktop)
- Intuitive navigation
- Modern UI/UX
- Accessibility standards (WCAG 2.1 Level A minimum)

#### NFR-03: Security
- Secure authentication
- SQL injection prevention
- XSS protection
- CSRF protection
- Secure password storage

#### NFR-04: Scalability
- Container-based deployment (Docker)
- Database connection pooling
- Static file caching
- API pagination

#### NFR-05: Maintainability
- Clean code architecture
- Comprehensive documentation
- Version control (Git)
- Modular design

---

## 3. Use Cases

### UC-01: View Portfolio (Public)
**Actor:** Visitor  
**Precondition:** None  
**Main Flow:**
1. Visitor mengakses website
2. System menampilkan homepage dengan hero section
3. Visitor scroll untuk melihat sections (About, Skills, Projects, Experience, Blog)
4. Visitor dapat filter/search projects
5. Visitor dapat melihat detail project
6. Visitor dapat like project
7. System update view counter

**Postcondition:** Project views dan likes ter-update

### UC-02: Send Contact Message (Public)
**Actor:** Visitor  
**Precondition:** None  
**Main Flow:**
1. Visitor mengisi contact form (name, email, subject, message)
2. Visitor submit form
3. System validate input
4. System save message to database
5. System menampilkan success confirmation

**Alternative Flow:**
- 3a. Validation fails → Show error message

**Postcondition:** Message tersimpan di database

### UC-03: Admin Login
**Actor:** Admin  
**Precondition:** Admin memiliki valid credentials  
**Main Flow:**
1. Admin mengakses admin page
2. System menampilkan login form
3. Admin input username dan password
4. System validate credentials
5. System generate JWT token
6. System redirect ke dashboard

**Alternative Flow:**
- 4a. Invalid credentials → Show error message

**Postcondition:** Admin logged in dengan valid session

### UC-04: Manage Projects (Admin)
**Actor:** Admin  
**Precondition:** Admin sudah login  
**Main Flow:**
1. Admin akses Projects section
2. System menampilkan list projects
3. Admin pilih action (Add/Edit/Delete)
4. Admin input/modify data (title, description, image, etc.)
5. Admin submit form
6. System validate dan save data
7. System update project list

**Postcondition:** Project data ter-update

### UC-05: Manage Skills (Admin)
**Actor:** Admin  
**Precondition:** Admin sudah login  
**Main Flow:**
1. Admin akses Skills section
2. System menampilkan list skills
3. Admin add new skill (name, level, icon, category)
4. Admin submit form
5. System save skill
6. System update skill list

**Alternative Flow:**
- 3a. Delete skill → Confirm deletion → System remove skill

**Postcondition:** Skill data ter-update

### UC-06: View Analytics (Admin)
**Actor:** Admin  
**Precondition:** Admin sudah login  
**Main Flow:**
1. Admin akses Dashboard
2. System fetch statistics
3. System display:
   - Total projects, views, likes, articles
   - Recent projects
   - Recent messages
   - Popular projects
4. Admin review data

**Postcondition:** None

---

## 4. Business Process Flow

### 4.1 Visitor Journey
```
Start → Landing Page → Browse Sections → 
  ├→ View Projects → Like/Comment
  ├→ View Skills
  ├→ View Experience
  ├→ Read Articles
  └→ Contact Form → Submit → End
```

### 4.2 Admin Content Management Flow
```
Login → Dashboard → 
  ├→ Manage Projects → Add/Edit/Delete → Save
  ├→ Manage Skills → Add/Delete → Save
  ├→ Manage Experiences → Add/Delete → Save
  ├→ Manage Articles → Add/Edit → Save
  └→ Review Messages → Mark as Read → End
```

### 4.3 Authentication Flow
```
Admin Access → Login Page → 
  Input Credentials → Validate → 
    ├→ Valid → Generate JWT → Dashboard
    └→ Invalid → Error Message → Retry
```

---

## 5. User Stories

### Epic: Portfolio Showcase
- **US-01:** As a visitor, I want to see featured projects on homepage, so I can quickly view best works
- **US-02:** As a visitor, I want to filter projects by category, so I can find relevant projects
- **US-03:** As a visitor, I want to search projects, so I can find specific projects quickly
- **US-04:** As a visitor, I want to see project details, so I can understand the project better
- **US-05:** As a visitor, I want to like projects, so I can show appreciation

### Epic: Skills & Experience
- **US-06:** As a visitor, I want to see skills with proficiency levels, so I can assess capabilities
- **US-07:** As a visitor, I want to see work experience timeline, so I can understand career journey
- **US-08:** As a recruiter, I want to see detailed experience descriptions, so I can evaluate qualifications

### Epic: Content Management
- **US-09:** As an admin, I want to easily add new projects, so I can keep portfolio updated
- **US-10:** As an admin, I want to upload images, so I can showcase projects visually
- **US-11:** As an admin, I want to manage skills, so I can reflect current expertise
- **US-12:** As an admin, I want to view analytics, so I can track portfolio performance

### Epic: Communication
- **US-13:** As a visitor, I want to send messages, so I can inquire about collaboration
- **US-14:** As an admin, I want to receive and manage messages, so I can respond to inquiries
- **US-15:** As a visitor, I want to see social media links, so I can connect on other platforms

---

## 6. Business Rules

### BR-01: Authentication
- Only authenticated admin can access admin panel
- Session expires after 24 hours of inactivity
- Password must be at least 8 characters

### BR-02: Content Visibility
- All visitors can view published content
- Unpublished articles only visible to admin
- Unapproved comments not shown to public

### BR-03: Data Validation
- All form inputs must be validated
- File uploads limited to specific types (images only)
- Maximum file size: 16MB
- Required fields must not be empty

### BR-04: Project Management
- Each project must have: title, description, image
- Projects can be marked as "featured"
- Categories must be predefined
- Tags are optional but recommended

### BR-05: Analytics
- View counter increments on each project view
- Likes can be given without authentication
- Statistics updated in real-time

---

## 7. Success Metrics

### 7.1 Key Performance Indicators (KPIs)
1. **Traffic Metrics**
   - Monthly unique visitors: Target 1000+
   - Page views per session: Target 5+
   - Average session duration: Target 3+ minutes

2. **Engagement Metrics**
   - Project likes: Target 50+/month
   - Contact form submissions: Target 10+/month
   - Article views: Target 500+/month

3. **Technical Metrics**
   - Page load time: < 3 seconds
   - Server uptime: > 99.5%
   - Error rate: < 1%

4. **Content Metrics**
   - Projects published: Target 20+
   - Articles published: Target 12+/year
   - Skills listed: Target 15+

### 7.2 Success Criteria
- ✅ Portfolio viewable on all devices
- ✅ Admin can manage content without technical knowledge
- ✅ Visitors can easily navigate and find information
- ✅ Fast and responsive user experience
- ✅ Secure and reliable system

---

## 8. Risk Analysis

### 8.1 Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Low visitor traffic | High | Medium | SEO optimization, social media marketing |
| Content becomes outdated | Medium | High | Regular content updates, set reminders |
| Competition | Medium | High | Unique design, quality content |
| Technical issues | High | Low | Monitoring, backup strategy |

### 8.2 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Server downtime | High | Low | Use reliable hosting, monitoring |
| Security breach | High | Low | Regular updates, security best practices |
| Data loss | High | Very Low | Regular backups, database replication |
| Performance degradation | Medium | Medium | Optimization, caching, CDN |

---

## 9. Assumptions and Constraints

### 9.1 Assumptions
- Admin has basic computer skills
- Users have modern web browsers
- Internet connectivity is available
- Server resources are adequate

### 9.2 Constraints
- Budget: Limited (using free/open-source technologies)
- Timeline: 2 weeks for MVP
- Team: 1 developer
- Technology: Docker, Python Flask, PostgreSQL

---

## 10. Future Enhancements

### Phase 2 Features
1. Multi-language support (Bahasa Indonesia & English)
2. Advanced analytics with charts
3. Comment system for blog posts
4. Project rating system
5. Newsletter subscription

### Phase 3 Features
1. Social media integration (auto-post)
2. Resume/CV download
3. Testimonials section
4. Project filtering by technology stack
5. Dark/Light mode toggle (fully functional)

### Phase 4 Features
1. Integration with GitHub API
2. Real-time chat support
3. Portfolio templates
4. Export portfolio as PDF
5. Admin mobile app

---

## 11. Approval and Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | Fitrah | _________ | 2025-12-13 |
| Business Analyst | Fitrah | _________ | 2025-12-13 |
| Developer | Fitrah | _________ | 2025-12-13 |

---

**Document Status:** Approved  
**Next Review Date:** January 13, 2026  
**Version History:**
- v1.0 (2025-12-13): Initial BSD document
