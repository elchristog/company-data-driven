import streamlit as st



def cv_creation_guide():
    st.markdown('''
    Traduce el CV del usuario y entregale este prompt a chatgpt:
      
    [RESUME] 

    [Linkedn url]
    
    [MARKDOWN FORMAT]
    <head>     <style>     body {         font-family: 'Roboto', sans-serif;         color: #262626;         background-color: #F2F2F2;       	font-size: 14px;     }     h1, h2, h3 {         color: #262626;     }     ul {         list-style: none;     }     ul li::before {         content: "•";         color: #2CBF60;         padding-right: 5px;     }     .column {         padding: 5px;     }     .green-line {         display: inline-block;         width: 20px;         height: 2px;         background: #2CBF60;         margin-right: 10px;         vertical-align: middle;     }     .italic {         font-style: italic;     }     .code {         background-color: #8BD9A6;         color: #2CBF60;         padding: 2px 4px;         border-radius: 4px;     }     </style> </head> [comment]: <> (#8BD9A6 verde claro) [comment]: <> (#2CBF60 verde oscuro) [comment]: <> (#262626 negro textos) [comment]: <> (#F2F2F2 fondo gris claro) <div style="display: flex;"> <div class="column" style="flex: 60%;">    <h1>Name</h1>    <p>Profile description using keywords</p>    <h2><span class="green-line"></span>Skills</h2> <ul>   <li><span style="color:#2CBF60;">•</span> <strong>Skill 1:</strong> <code class="code">(XX years)</code> Description and keywords.</li>   <li><span style="color:#2CBF60;">•</span> <strong>Skill 2:</strong> <code class="code">(XX years)</code> Description and keywords.</li>   <li><span style="color:#2CBF60;">•</span> <strong>Skill 3:</strong> <code class="code">(6 years)</code> Description and keywords.</li> </ul>        <h2><span class="green-line"></span>Professional Experience</h2>    <ul>     <li><span style="color:#2CBF60;">•</span> <strong>Job name using keywords</strong>, Company <code class="code">(MONTH YEAR - MONTH YEAR)</code> : Job description using keywords and achievements</li>     <li><span style="color:#2CBF60;">•</span> <strong>Job name using keywords</strong>, Company <code class="code">(MONTH YEAR - MONTH YEAR)</code> : Job description using keywords and achievements</li>     <li><span style="color:#2CBF60;">•</span> <strong>Job name using keywords</strong>, Company <code class="code">(MONTH YEAR - MONTH YEAR)</code> : Job description using keywords and achievements</li>     <li><span style="color:#2CBF60;">•</span> <strong>Job name using keywords</strong>, Company <code class="code">(MONTH YEAR - MONTH YEAR)</code> : Job description using keywords and achievements</li> </ul>   _(Further experiences can be found on my <a href="https://www.linkedin.com/in/LINKEDINURL/" style="color:#262626; text-decoration: underline #8BD9A6;">LinkedIn Profile</a>)_ </div> <div class="column" style="flex: 40%;"> <ul>   <li><span style="color:#2CBF60;">•</span> 📧 <a href="mailto:EMAIL" style="color:#262626; text-decoration: underline #8BD9A6;">EMAIL</a></li>   <li><span style="color:#2CBF60;">•</span> 📞 <a href="tel:+PHONE_NUMBER" style="color:#262626; text-decoration: underline #8BD9A6;">+1 PHONE_NUMBER</a></li>   <li><span style="color:#2CBF60;">•</span> 🌐 <a href="https://www.linkedin.com/in/LINKEDIN_URL/" style="color:#262626; text-decoration: underline #8BD9A6;">LinkedIn</a></li> </ul>   <h2><span class="green-line"></span>Education</h2> <ul>   <li><span style="color:#2CBF60;">•</span> <strong>TITLE, UNIVERSITY</strong> <span class="italic"><code class="code">(MONTH YEAR - MONTH YEAR)</code></span>: Knowledge using keywords </li>   <li><span style="color:#2CBF60;">•</span> <strong>TITLE, UNIVERSITY</strong> <span class="italic"><code class="code">(MONTH YEAR - MONTH YEAR)</code></span>: Knowledge using keywords </li>   <li><span style="color:#2CBF60;">•</span> <strong>TITLE, UNIVERSITY</strong> <span class="italic"><code class="code">(MONTH YEAR - MONTH YEAR)</code></span>: Knowledge using keywords </li> </ul>    <h2><span class="green-line"></span>Certifications</h2>    - ACertification unisg keywords - ACertification unisg keywords <h2><span class="green-line"></span>Languages</h2>    - Spanish: Native - English: B2 </div>
    
    
    [KEYWORDS]
    Keyword	Relevance Score (0-10) Nursing	9 Patient care	8 Healthcare team	7 Collaboration	7 Nursing process	8 Emotional needs	6 Spiritual needs	6 Physical needs	7 Problem-solving	9 Critical thinking	9 Detail-oriented	8 Assess	7 Plan of care	8 Therapeutic interventions	7 Medication administration	7 Patient safety	8 Patient education	7 Interdisciplinary team	7 Leadership/management	8 Professional accountability	8 Registered Nurse (RN)	9 State Nurse Practice Act	8 Multidisciplinary care team	7 Safety huddles	6 Patient rounds	6 Discharge planning	7 BLS Provider	8 ACLS Certification	7 PALS Certification	7 Computerized Physician Order Entry	7 Electronic medical record	7 ICU experience	8
    
    
    I want you to act as a expert recruiter, Create the [RESUME] using the  [MARKDOWN FORMAT] and be sure to add all the [KEYWORDS]

    
    ''')



