# MongoDB Core Concepts & CRUD Operations

## 1. The Document Model
[cite_start]Unlike relational databases that use rigid tables and rows, MongoDB is a NoSQL database that uses **Collections** and **Documents**[cite: 343, 344].
* [cite_start]**Database:** A physical container for collections[cite: 345].
* [cite_start]**Collection:** A group of documents (equivalent to an RDBMS table)[cite: 346]. [cite_start]They do not enforce a rigidschema[cite: 353].
* [cite_start]**Document:** A record consisting of JSON-like key-value pairs (equivalent to a row)[cite: 348].
* **`_id` Field:** Every document requires a unique `_id`.[cite_start]If not provided, MongoDB auto-generates a 12-byte hexadecimal ObjectId[cite: 361, 362].

## 2. CRUD: Read (Finding Data)
[cite_start]The basic command to retrieve documents is `find()`[cite: 506, 1016].
* [cite_start]**Syntax:** `db.<collection>.find(filter, projection)`[cite: 1021].
* **Find All:** `db.students.find({})`[cite: 1031].
* [cite_start]**Prettify Output:** Append `.pretty()` to format the JSON nicely (e.g., `db.students.find().pretty()`)[cite: 507].
* **Comparison Operators:**
    * [cite_start]`$eq`: Equals [cite: 1157]
    * [cite_start]As a shorthand, MongoDb assumes equality by default if you don't provide an operator. Example: db.students.find({ "name": "Liza" })
    * `$lt` / `$lte`: Less than / Less than or equal to [cite: 1152, 1153]
    * [cite_start]`$gt` / `$gte`: Greater than / Greater than or equal to [cite: 1154, 1155]
    * [cite_start]`$ne`: Not equal to [cite: 1156]
    * *Example:* `db.students.find({ "gpa": { $gte: 3.5} })`

## 3. CRUD: Create (Inserting Data)
* [cite_start]**Insert One:** `db.<collection>.insertOne(document)`[cite: 491, 1034].
* [cite_start]**Insert Mny:** `db.<collection>.insertMany([doc1, doc2])`[cite: 492, 1035]. Uses an array of documents.
## 4. CRUD: Update (Modifying Data)
[cite_start]Updates require a filter to find the document, and an update operation to tell it what to change[cite: 1075, 1076].
* [cite_start]**`updateOne(<filter>, <update>)`:** Updates only the first matching document[cite: 1081, 1083].
* **`updateMany()`:** Updates all matching documents[cite: 1086].
* To update every document in a collection, you can pass an empty document {} as the filter.
* **Update Operators:**
     * `$set`: Replaces the value of a field[cite: 1079, 1097].
     * [cite_start]`$inc`: Increases a number by a specified value[cite: 1098, 1118].
     * *Example:* `db.courses.updateOne({ "course": "CMPUT 291" }, { $set: { "seats": 50} })`

## 5. CRUD: Delete (Removing Data)
* [cite_start]**`deleteOne(filter)`:** Deletes only the first document that matches the condition[cite: 1146, 1147].
* **`deleteMany(filter)`:** Deletes all documents that match the filter[cite: 1148, 1149].
* [cite_start]*Warning:8 `db.<collection>.delete({})` will remove all documents in the collection[cite: 565].

## 6. Aggregation Pipelines
The aggregation framework allows you to process data records and return computed results. [cite_start]Documents pass through a multi-stage pipeline, getting filtered or transformed at each step[cite: 1509,1515].

* [cite_start]**Basic Syntax:** `db.<collection>.aggregate([ {stage1}, {stage2}, ...]` [cite: 1580, 1582, 1584]

### Core Pipeline Stages:
* [cite_start]**`$match`:** Filters documents to pass only those that match the specified condition(s) to the next stage[cite: 1924, 1925, 1928]. [cite_start]It uses the exact same syntax as standard read  operations[cite: 1530]. *Best Practice: Place `$match` as early as possible in the pipeline to reduce the amount of data being processed.*
* **`$project`:** Reshapes each document in the stream, such as by adding new fields or removing existing ones. [cite_start]Use '1' to include a field and '0' to exclude it[cite: 82, 84].
* [cite_start]**`$group`:** Groups input documents by a specified `_id` expression and applies accumulator expressions to each group[cite: 1683].
    * [cite_start]*Common Accumulators:* `$sum`, `$avg`, `$max`, `$min`[cite: 172, 636, 637].
    * Example: db.students.aggregate([ { $group: {_id: "$year", avgGPA: { $avg: "$gpa" }}}])
    * `_id: "$year"`: Tells the pipeline to look at the year field and create a distinct group for every unique year it finds.
    * avgGPA: name given to the brand new computed field
    * `{ $avg: "$gpa" }`: this is an accumulator. For every document that gets sorted into a specific year's group, MongoDB takes the value of its gpa field and calculates the average for the whole group
* [cite_start]**`$sort`:** Reorders the document stream by a specified field (`1` for ascending, `-1` for descending)[cite: 154].
* [cite_start]**`$limit`:** Restricts the number of documents passed to the next stage[cite: 1652, 1653].

### Advanced Pipeline Stages: Dealing with Arrays
When a document contains an array (like a list of courses or tags), grouping and filtering can get tricky. To solve this, we use the `$unwind` stage.

* [cite_start]**`$unwind`:** Deconstructs an array field from the input documents to output a document for *each* element[cite: 48].
     * [cite_start]*Example:* If Liza is taking `['CMPUT 379', 'CMPUT 291']`, `$unwind` turns her single document into **two** separate documents: one for 379 and one for 291[cite: 49, 58].

### Example: Average Year of Students in a Course
TO find the average year of students taking CMPUT 291, the pipeline looks like this:
1. [cite_start]**Unwind:** Flatten the `courses_taken` array[cite: 189].
2. [cite_start]**Match:** Filter for only "CMPUT 291"[cite: 190].
3. [cite_start]**Group:** Group by the course and use the `$avg` accumulator on the `$year` field.

```javascript
db.students.aggregate([ { $unwind: "$courses_taken" }, { $match: { courses_taken: "CMPUT 291" }} , { $group: { _id: "$courses_taken", avg_year: { $avg: : "$year"}}} ])


### Putting it all together: Multi-Stage Pipelines
To perform complex data analysis, you can chain multiple stages together in an array. The output of one stage becomes the input for the next.

**Example: Find the highest-performing courses by average GPA**
```javascript
db.students.aggregate([ { $unwind: "courses_taken"}, { $group: { _id: "course_taken", avg_GPA: { $avg: "$gpa"}}}, { $sort: { avg_GPA: -1}} ])
