# CMPUT 291: MongoDB Study & Mini-Project Prep

This repository contains my study notes, practice queries, and Python integration scripts for MongoDB. This environment was built to master the core concepts required for the CMPUT 291 File and Database Management Systems final mini-project.

## 🚀 Repository Contents

* **`study_notes.md`**: Comprehensive documentation covering:
  * The MongoDB Document Model
  * Core CRUD Operations (Create, Read, Update, Delete)
  * Multi-stage Aggregation Pipelines (`$match`, `$group`, `$unwind`, `$sort`)
  * PyMongo syntax and cursor iteration
* **`course_analytics.py`**: A Python script demonstrating how to connect to a local MongoDB server and execute complex aggregation pipelines using `pymongo`.
* **`test_connection.py`**: A lightweight script to verify database connectivity and basic querying.

## 🛠️ Technologies & Tools
* **Database:** MongoDB
* **Language:** Python 3
* **Libraries:** PyMongo
* **Environment:** Executed on UAlberta Lab Machines via SSH

## ⚙️ Quick Start Setup

To replicate this environment and run the scripts:

1. **Start the MongoDB Server:**
   Run the server in the background on a designated port.
   ```bash
   mongod --port 27012 --dbpath ~/mongodb_data_folder &```

2. **Import Sample Data:**
   bash
  ```mongoimport --port 27012 --db csdb --collection students --file students.json --jsonArray```

3. Install Dependencies:
  bash
  ```python3 -m pip install pymongo```

4. Run the Analytics Script:
   ```bash
   python3 course_analytics.py```
