### User Story: Pet Walking SaaS App

#### Overview

This Pet Walking SaaS app connects pet owners with certified, local dog walkers. The app uses an advanced algorithm to match owners with walkers based on location, availability, pet care qualifications, pricing preferences, and other personal qualifications. Both owners and walkers can set preferences, receive notifications, and complete payments securely within the app. The following user story outlines the main and alternative journeys for two primary personas: a pet owner and a pet walker.

---

### **Primary Personas**

1. **Pet Owner (Sophie, 32)**

   - **Motivation**: Sophie wants to ensure her dog, Max, gets regular walks during the day while she’s at work. She prefers walkers who are near her home or work, have experience with large dogs, and can offer services within her budget.
   - **Frustrations**: Sophie has struggled with inconsistent availability and lack of reliable, qualified walkers.
   - **Goal**: To find a reliable, qualified walker who can handle her dog on a recurring schedule and fits her budget.

2. **Pet Walker (David, 28)**
   - **Motivation**: David is a professional dog walker and trainer who wants to expand his client base. He wants to be matched with pet owners who are nearby, have pets within his handling experience, and are looking for regular appointments.
   - **Frustrations**: David has found it challenging to coordinate schedules with owners and wants to minimize time traveling between jobs.
   - **Goal**: To book consistent, well-paying jobs with clients who appreciate his professional qualifications and live nearby.

---

### **User Journeys**

#### **User Journey 1: Pet Owner Sophie Matching with a Walker**

1. **Sign Up & Profile Creation**

   - Sophie creates a profile by inputting her personal information, pet details (e.g., Max’s breed, age, weight), preferences for walks (e.g., time, distance, frequency), and her budget range.
   - She verifies her location, syncing with her phone’s GPS, and enters her preferred areas for pick-up and drop-off.

2. **Setting Availability**

   - Sophie selects her preferred days and time slots for Max’s walks, syncing the app with her Google Calendar for accuracy.

3. **Finding a Match**

   - Sophie inputs a new walking request, including her desired start date and recurring schedule.
   - The app’s algorithm runs and presents Sophie with a list of compatible walkers based on:
     - **Location proximity** (walkers near Sophie’s home or workplace)
     - **Walkers' experience** with large dogs like Max
     - **Availability** matching her desired schedule
     - **Price** within her selected budget range

4. **Reviewing Walkers**

   - Sophie can review each walker’s profile, including:
     - Star ratings from previous clients
     - Certification badges (e.g., pet CPR certification, large-dog handling)
     - Price per walk or per hour
   - Sophie picks David, a walker with a 5-star rating, who specializes in large dogs, is within her budget, and is close to her home.

5. **Booking & Payment**

   - Sophie confirms the booking with David for 3 walks per week at $30 per walk.
   - Payment is processed securely within the app, with the option to set up automatic payments for recurring services.

6. **Notifications & Follow-up**
   - Sophie receives a notification when David starts and ends the walk.
   - After the walk, David sends a summary and photos of Max, and Sophie rates the walk.

---

#### **User Journey 2: Pet Walker David Receiving a Request**

1. **Sign Up & Profile Creation**

   - David creates his profile, inputting his experience, qualifications, price range, availability, and preferred areas for walking.
   - He provides verification for certifications and uploads background check documents for additional trustworthiness.

2. **Setting Availability**

   - David sets his walking hours for Monday through Friday, syncing his availability with the app.
   - He also marks preferred neighborhoods, minimizing his travel time between jobs.

3. **Receiving a Match**

   - The app sends a notification to David when a potential match is found based on:
     - **Location proximity** to the owner’s residence or walking area
     - **Pet type** (David has specified he prefers larger dogs like Max)
     - **Price** (David’s rate is within Sophie’s budget)
     - **Availability** matching the owner's request

4. **Reviewing the Request**

   - David reviews Sophie’s request, including details about Max, her expectations, and the recurring schedule.
   - He decides to accept the request, as it fits well with his schedule and expertise.

5. **Confirmation**

   - David confirms the booking for the first walk and agrees to recurring walks for the following week.
   - He receives a pre-walk notification and prepares for the appointment.

6. **During and After the Walk**
   - During the walk, David uses the app’s built-in GPS tracker, which allows Sophie to see live updates.
   - After the walk, David logs the walk’s duration and sends feedback about Max’s behavior along with photos.

---

### **Alternate User Journey: Sophie Needs to Cancel a Walk**

1. **Canceling a Walk**
   - Sophie needs to cancel a scheduled walk. She opens the app, navigates to the "Upcoming Walks" section, and selects the walk she wants to cancel.
   - Sophie can choose to either reschedule the walk or cancel it altogether. If the cancellation is within the allowed window (e.g., 24 hours before), she does not incur a fee. If it’s too close to the scheduled time, she is charged a cancellation fee as per David’s policy.

---

### **Acceptance Criteria**

1. **User Registration & Profile**

   - Users can create and verify their profiles (owners and walkers) using an email or social media account.
   - Pet details must be completed, including breed, size, age, and special care needs.
   - Walkers must upload verification documents for any qualifications and pass a background check.

2. **Matching Algorithm**

   - The algorithm must consider multiple factors: location, availability, pricing, pet-specific qualifications, and reviews/ratings.
   - The algorithm should display the top 3-5 walkers for owners to choose from, with clear indications of why they are the best matches.

3. **Booking & Payment**

   - Owners can book and pay for single or recurring walks via the app.
   - Walkers receive notifications of requests and must confirm or decline within a set time.
   - Payments must be processed securely, with the ability to set recurring payments.

4. **Walk Completion Tracking**

   - GPS tracking should be active during each walk, visible to both the owner and walker.
   - Walkers must log the walk’s start and end time, and owners receive notifications.
   - Walkers should be able to leave feedback and send media (photos/videos) after each walk.

5. **Cancellations**
   - Owners can cancel walks within a set timeframe without penalty.
   - If owners cancel outside the allowed time, a cancellation fee is charged.

---

### **Exceptions & Edge Cases**

1. **No Walkers Available**

   - If the algorithm finds no available walkers meeting Sophie’s criteria, it should suggest expanding the search area, adjusting the schedule, or increasing the budget.
   - Alternatively, it can offer to notify Sophie when a new walker matching her preferences becomes available.

2. **Walker Canceling a Booking**

   - If David needs to cancel a walk, Sophie receives an immediate notification with alternative walkers suggested by the app.
   - Sophie can either choose a new walker for that session or reschedule with David.

3. **Payment Failure**

   - If Sophie’s payment fails, she receives a notification, and the booking is held for 24 hours before being canceled.
   - Walkers are notified that payment is pending, and the walk remains tentatively scheduled.

4. **Discrepancy in Walk Duration**
   - If there’s a discrepancy in the walk’s logged duration, the owner and walker can dispute the charge via the app. A dispute resolution process will review GPS logs and notifications.

---

This user story details a seamless experience for both pet owners and walkers, with user-friendly features and an intelligent algorithm to enhance matching accuracy and efficiency.
