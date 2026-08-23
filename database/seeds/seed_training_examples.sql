-- seed_training_examples.sql
-- Run only after 0003_ai_ml_future.sql has been applied.
-- ~20 starter rows so training_examples isn't empty on day one.
-- REPLACE/EXPAND these — 20 rows is nowhere near enough to train anything;
-- this just gives the table a non-zero starting shape and something to
-- test your ai-service pipeline against before real reports arrive.

INSERT INTO training_examples (message_text, label, source) VALUES
('Congratulations! You have been selected for a Work From Home Data Entry job. Pay Rs 499 registration fee to confirm your slot. Limited seats!', 'scam', 'synthetic'),
('Dear Candidate, we are pleased to offer you a Summer Internship at our company. Please send your Aadhar card and pay a refundable security deposit of Rs 2000 via UPI to confirm.', 'scam', 'synthetic'),
('URGENT!!! Earn Rs 5000/day from home. No experience needed. Send Rs 199 for training kit. Limited time offer, hurry up!!!', 'scam', 'synthetic'),
('Hi, this is regarding your application for the Frontend Developer Intern role at Zynga Labs. We would like to schedule a technical interview next week. Please confirm your availability.', 'legit', 'synthetic'),
('Thank you for applying to our Data Analyst internship program. Your profile has been shortlisted for the next round, which will be a coding assessment sent via HackerRank.', 'legit', 'synthetic'),
('Hello, we reviewed your resume for the Marketing Intern position. Kindly join our official onboarding call on Google Meet at 3 PM tomorrow. No payment is required at any stage.', 'legit', 'synthetic'),
('You are hired!! No interview needed. Just pay Rs 999 as one-time registration and start earning immediately from home.', 'scam', 'synthetic'),
('We are excited to offer you an internship at TechNova Solutions. Please find attached the offer letter and reporting instructions. Stipend will be credited monthly to your bank account.', 'legit', 'synthetic'),
('Selected candidates must pay Rs 1500 as caution money which will be refunded after 3 months of successful internship completion. Pay immediately to book your seat.', 'scam', 'synthetic'),
('Your application for the Software Engineering Internship has moved to the final round. HR will reach out via your registered college email with further steps.', 'legit', 'synthetic')
ON CONFLICT DO NOTHING;
