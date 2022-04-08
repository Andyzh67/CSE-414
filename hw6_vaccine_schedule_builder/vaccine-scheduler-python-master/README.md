# Python Application for Vaccine Scheduler

This project simulates an appointment scheduler for vaccinations, where the users (patients and caregivers) can keep
track of vaccine stock and appointments.

This application runs on the command line terminal, and this reservation system is also connected to a Microsoft Azure Database.

- src.main.resources
  - design.pdf: design of the database schema.
  - create.sql: create statement for the tables.

- src.main.scheduler.model
  - Caregiver.py: data model for the caregivers.
  - Patient.py: data model for the users.
  - Vaccine.py: data model the vaccines.

- src.main.scheduler
  - Scheduler.py: main runner for the command-line interface.
