CS 340 Portfolio Reflection – Rakim Spriggs
Maintainable, Readable, and Adaptable Code

Writing maintainable, readable, and adaptable programs starts with organization and separation of responsibilities. In this course, I applied this approach by creating a standalone CRUD Python module in Project One and then reusing it in Project Two to connect the dashboard to the MongoDB database. This separation made the code easier to read and update because database logic was isolated from the user interface.

The advantage of this approach is that the CRUD module can be reused in other applications without rewriting database connection logic. For example, I could use this same module in a future web app, mobile backend, or analytics tool that needs to interact with MongoDB. It also makes debugging easier because issues can be traced to either the database layer or the front-end layer independently.

Approaching Problems as a Computer Scientist

When approaching the requirements for the Grazioso Salvare dashboard, I broke the problem into smaller parts: database setup, data retrieval, filtering logic, and visualization. This structured approach allowed me to focus on one component at a time rather than trying to build everything at once.

Compared to previous assignments, this project required more integration between systems rather than solving isolated problems. I had to think about how data flows from the database to the user interface and how user actions trigger updates. In the future, I would continue using this modular and step-by-step approach, especially when designing databases for client needs. I would also spend more time planning schema design and query efficiency before implementation.

The Role of Computer Scientists and Why It Matters

Computer scientists design systems that help organizations make better decisions using data. In this project, the dashboard allows Grazioso Salvare to quickly identify dogs that meet specific rescue criteria. Instead of manually searching through records, the company can filter and visualize data instantly.

This type of work matters because it improves efficiency, accuracy, and decision-making. By building tools like this dashboard, computer scientists enable organizations to focus on their core mission—in this case, training rescue animals—while relying on technology to handle data analysis.

Conclusion

This project demonstrates how combining databases, programming, and user interfaces can create practical solutions for real-world problems. The skills developed in this course, including working with MongoDB, building reusable modules, and designing interactive dashboards, will be valuable for future projects and professional work.
