# ============================================================
# scenarios.py — 10 Test Scenarios + Human Reference Emails
# ============================================================
# Each scenario contains:
#   id        : unique identifier (1–10)
#   intent    : the core purpose of the email
#   facts     : list of key facts that MUST appear in the email
#   tone      : desired style/register
#   reference : the ideal "human written" reference email

SCENARIOS = [
    {
        "id": 1,
        "intent": "Follow up after a job interview for a Senior Machine Learning Engineer position",
        "facts": [
            "The interview took place last Monday",
            "The position is Senior Machine Learning Engineer",
            "Enjoyed the discussion about NLP projects and transformer architectures",
            "Available to start within two weeks of receiving an offer",
            "Happy to provide additional references or work samples if needed"
        ],
        "tone": "professional and enthusiastic",
        "reference": """Subject: Following Up – Senior ML Engineer Interview (Last Monday)

Dear [Hiring Manager's Name],

Thank you so much for taking the time to meet with me last Monday to discuss the Senior Machine Learning Engineer position. It was a genuine pleasure to speak with you and the team.

I particularly enjoyed our conversation about your NLP projects and the work being done with transformer architectures. The ambition of your roadmap only reinforced my excitement about contributing to the team.

I remain very enthusiastic about this opportunity and wanted to confirm that I am available to start within two weeks of receiving an offer. Please don't hesitate to reach out if you need additional references or work samples to support your decision.

I look forward to hearing from you.

Warm regards,
[Your Name]
[Your Email] | [Your Phone]"""
    },
    {
        "id": 2,
        "intent": "Schedule a product demo meeting with a potential enterprise client",
        "facts": [
            "The product is an AI-powered analytics dashboard called InsightFlow",
            "The demo lasts 30 minutes",
            "Available slots are Monday through Wednesday next week",
            "The demo will showcase the ROI calculator and real-time reporting features",
            "The client company is TechCorp Solutions"
        ],
        "tone": "formal and confident",
        "reference": """Subject: InsightFlow Demo Request – Scheduling for Next Week

Dear [Contact Name],

I hope this message finds you well. I am writing to propose a 30-minute demonstration of InsightFlow, our AI-powered analytics dashboard, tailored specifically for organizations like TechCorp Solutions.

During the session, we will walk you through our real-time reporting capabilities and our proprietary ROI calculator — both of which have delivered measurable value for our enterprise clients. We are confident you will find these features directly relevant to your operational goals.

We have availability Monday through Wednesday of next week and would be happy to accommodate a time that suits your schedule. Please let us know your preferred slot and we will send a calendar invite with all details.

We look forward to the opportunity to show what InsightFlow can do for TechCorp Solutions.

Yours sincerely,
[Your Name]
[Title] | [Company Name]
[Email] | [Phone]"""
    },
    {
        "id": 3,
        "intent": "Notify a client about an unexpected project delay and provide a revised timeline",
        "facts": [
            "The original delivery deadline was June 15",
            "The new revised deadline is July 1",
            "The delay was caused by unexpected API integration issues with a third-party vendor",
            "Two additional engineers have been allocated to accelerate delivery",
            "Weekly status updates will be provided going forward"
        ],
        "tone": "apologetic and professional",
        "reference": """Subject: Project Update – Revised Delivery Timeline

Dear [Client Name],

I am writing to inform you of an unexpected delay affecting your project delivery, and I sincerely apologize for the inconvenience this causes.

Due to unforeseen API integration issues with our third-party vendor, we are unable to meet the original June 15 deadline. After a thorough assessment, our revised delivery date is July 1. We understand the impact this has on your planning and deeply regret the disruption.

To address this as swiftly as possible, we have allocated two additional engineers to the project, effective immediately. You can expect weekly status updates from our team to ensure full transparency throughout the remainder of the engagement.

We are committed to delivering a high-quality result and appreciate your patience. Please feel free to contact me directly with any questions.

Sincerely,
[Your Name]
[Title] | [Company Name]
[Email] | [Phone]"""
    },
    {
        "id": 4,
        "intent": "Introduce a new data scientist joining the team to all staff",
        "facts": [
            "Her name is Dr. Sarah Chen",
            "Her role is Senior Data Scientist",
            "She starts this coming Monday",
            "She has 5 years of experience at Google DeepMind",
            "Her primary expertise is in computer vision and generative AI"
        ],
        "tone": "warm and welcoming",
        "reference": """Subject: Welcome Dr. Sarah Chen – New Senior Data Scientist Joining Monday!

Hi Team,

I'm thrilled to share some exciting news — we have a fantastic new colleague joining us this Monday!

Please join me in welcoming Dr. Sarah Chen, who will be stepping into the role of Senior Data Scientist. Sarah comes to us with five impressive years of experience at Google DeepMind, where she developed deep expertise in computer vision and generative AI. Her background is an incredible asset and I have no doubt she will make a real impact on our work.

Please take a moment to introduce yourself when she arrives on Monday and help make her feel right at home. I'm also happy to facilitate any introductions beforehand if you'd like to connect early.

Let's give Sarah a wonderful welcome — we're so glad to have her!

Best,
[Your Name]"""
    },
    {
        "id": 5,
        "intent": "Request a formal proposal and pricing quote from a cloud storage vendor",
        "facts": [
            "The company needs a cloud storage solution for 50TB of data",
            "The solution must support 10 concurrent users",
            "Implementation is needed by Q3 of this year",
            "The company is open to flexible pricing models",
            "The proposal should include security certifications and uptime guarantees"
        ],
        "tone": "formal and direct",
        "reference": """Subject: Request for Proposal – Cloud Storage Solution (50TB)

Dear [Vendor Contact Name],

I am writing to request a formal proposal and pricing quote for a cloud storage solution that meets our current and projected data requirements.

Our specifications are as follows:
- Storage capacity: 50TB
- Concurrent users: 10
- Target implementation date: Q3 of this year

We are open to flexible pricing models, including subscription-based or tiered plans, and welcome your recommendation on the most cost-effective option for an organization of our scale.

Please include in your proposal details on uptime guarantees, data security certifications, scalability options, and onboarding support. We would appreciate your response within five business days.

Thank you for your time. We look forward to reviewing your proposal.

Regards,
[Your Name]
[Title] | [Company Name]
[Email] | [Phone]"""
    },
    {
        "id": 6,
        "intent": "Follow up after meeting a researcher at a conference and propose a collaboration",
        "facts": [
            "Met at NeurIPS 2024 in Vancouver",
            "Had a conversation about AI safety and alignment research",
            "Would like to explore a potential research collaboration",
            "Has a relevant published paper on reward modeling to share",
            "Open to a 30-minute virtual coffee chat in the coming weeks"
        ],
        "tone": "friendly and professional",
        "reference": """Subject: Great Meeting You at NeurIPS 2024 – Let's Stay in Touch!

Hi [Name],

It was a real pleasure meeting you at NeurIPS 2024 in Vancouver last week! Our conversation about AI safety and alignment was one of the highlights of the conference for me, and I've been looking forward to following up.

I think there's genuine potential for collaboration in this space, and I'd love to explore that further. In the meantime, I've attached a paper I recently published on reward modeling — I think you'll find it relevant to what we discussed and would genuinely value your thoughts.

Would you be open to a 30-minute virtual coffee chat in the coming weeks? I'm flexible on timing and happy to work around your schedule.

Looking forward to hearing from you!

Best,
[Your Name]
[Title] | [Institution/Company]
[Email] | [LinkedIn]"""
    },
    {
        "id": 7,
        "intent": "Escalate an unresolved customer support ticket to senior management",
        "facts": [
            "Support ticket number is #45892",
            "The ticket has been open and unresolved for 2 weeks",
            "The issue involves a critical payment processing failure",
            "The company is losing approximately $500 per day due to this issue",
            "Multiple follow-up attempts have been made with no resolution"
        ],
        "tone": "urgent and assertive",
        "reference": """Subject: URGENT ESCALATION – Ticket #45892: Payment Processing Failure (2 Weeks Unresolved)

Dear [Manager's Name],

I am writing to formally escalate Support Ticket #45892, which has remained unresolved for two weeks despite multiple follow-up attempts. This situation requires immediate senior-level attention.

The issue — a critical payment processing failure — is causing direct, ongoing financial damage to our operations. We are losing approximately $500 per day, representing a cumulative loss exceeding $7,000 over the past two weeks, with the figure growing every day the issue goes unresolved.

Despite repeated follow-ups through your standard support channels, we have received no viable resolution or committed timeline. This level of inaction is unacceptable for a business-critical failure of this magnitude.

I am formally requesting that Ticket #45892 be assigned to a dedicated senior engineer, with a status update provided within 24 hours.

I am available to discuss immediately.

Regards,
[Your Name]
[Title] | [Company Name]
[Email] | [Phone]"""
    },
    {
        "id": 8,
        "intent": "Request a deadline extension for a team project submission",
        "facts": [
            "The original submission deadline is this Friday",
            "Requesting a 3-day extension, new deadline would be Monday",
            "A key team member was unexpectedly hospitalized this week",
            "The project is approximately 80% complete",
            "The team is committed to maintaining full quality of the final deliverable"
        ],
        "tone": "polite and formal",
        "reference": """Subject: Deadline Extension Request – [Project Name]

Dear [Supervisor/Professor Name],

I hope this message finds you well. I am writing to respectfully request a short extension for our project submission, currently due this Friday.

Unfortunately, one of our key team members was unexpectedly hospitalized earlier this week, significantly impacting our capacity to complete the remaining work on schedule. Despite this unforeseen circumstance, I'm pleased to report that the project is approximately 80% complete and progressing well.

We are requesting a three-day extension, which would move the submission deadline to the following Monday. This time would allow us to maintain the standard of quality we take great pride in delivering.

We fully understand that extensions are not always possible and sincerely appreciate your consideration. Please let us know if you require any supporting documentation.

Thank you for your understanding.

Yours sincerely,
[Your Name]
[Email] | [Phone]"""
    },
    {
        "id": 9,
        "intent": "Send a cold outreach email proposing a B2B partnership to a fintech company",
        "facts": [
            "The sender's company is DataFlow Inc.",
            "DataFlow's product automates ML pipelines and reduces deployment time by 60%",
            "The target company operates in the fintech space — a shared target market",
            "Proposing a co-marketing and revenue sharing partnership model",
            "Requesting a 20-minute exploratory call to discuss the opportunity"
        ],
        "tone": "confident and persuasive",
        "reference": """Subject: Partnership Opportunity – DataFlow Inc. x [Company Name]

Dear [Contact Name],

My name is [Your Name] from DataFlow Inc. — we build ML pipeline automation tools that help engineering teams reduce model deployment time by up to 60%.

I came across [Company Name] while researching leaders in the fintech space and believe there's a compelling opportunity for us to collaborate. Given that we serve overlapping markets, a co-marketing and revenue sharing partnership could allow both companies to expand reach while delivering greater value to our shared customer base.

Our fintech clients consistently cite faster ML deployment as a critical competitive advantage, and combining DataFlow's capabilities with [Company Name]'s expertise could be a powerful market proposition.

I'd love to schedule a 20-minute exploratory call to discuss what a partnership might look like. Would you have availability in the coming week?

Best regards,
[Your Name]
[Title] | DataFlow Inc.
[Email] | [LinkedIn] | [Website]"""
    },
    {
        "id": 10,
        "intent": "Announce a new hybrid remote work policy to all non-technical staff",
        "facts": [
            "The new policy requires 3 days in-office per week",
            "The policy takes effect on August 1st",
            "The policy applies exclusively to non-technical staff",
            "Technical staff will receive separate communication with their own guidelines",
            "All questions and concerns should be directed to the HR department"
        ],
        "tone": "clear and authoritative",
        "reference": """Subject: Important Policy Update: New Hybrid Work Schedule – Effective August 1st

Dear Team,

We are writing to inform all non-technical staff of an important update to our workplace attendance policy, effective August 1st.

Beginning on that date, all non-technical employees will be required to work from the office a minimum of three (3) days per week. We believe this hybrid model strikes the right balance between the flexibility of remote work and the collaborative benefits of in-person presence. Specific in-office days may be coordinated with your direct manager.

Please note that this policy applies exclusively to non-technical staff. Technical teams will receive a separate communication with guidelines tailored to their roles.

We want to ensure you have all the support you need during this transition. Please direct any questions or concerns to the HR department, who are available to assist you.

Thank you for your continued commitment and cooperation.

Regards,
[Leadership/HR Name]
[Title] | [Company Name]"""
    }
]
