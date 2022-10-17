# week-5 作業

## 要求二

### 1.建立一個新的資料庫，取名字為 website。

![](images/Q2-1.png)
&emsp;

### - 使用 website 資料庫。

![](images/Q2-1-1.png)
&emsp;

### 2.在資料庫中，建立會員資料表，取名字為 member。

![](images/Q2-2.png)
&emsp;

### - 修改COMMENT文字內容。

![](images/Q2-2-1.png)
&emsp;

---

## 要求三

**1.使用INSERT指令新增資料至 member 資料表中。

![](images/Q3-1.png)
&emsp;

### 2.使用 SELECT 指令取得所有在 member 資料表中的會員資料。

![](images/Q3-2.png)
&emsp;

### 3.使用 SELECT 指令取得所有在 member 資料表中的會員資料，並按照 time 欄位，由近到遠排序。

![](images/Q3-3.png)
&emsp;

- (加入列數便於檢視結果)

![](images/Q3-3-1.png)
&emsp;

### 4.使用 SELECT 指令取得 member 資料表中第 2 ~ 4 共三筆資料，並按照 time 欄位，由近到遠排序。

![](images/Q3-4.png)
&emsp;

- (加入列數便於檢視結果)

![](images/Q3-4-1.png)
&emsp;

### 5.使用 SELECT 指令取得欄位 username 是 test 的會員資料。

![](images/Q3-5.png)
&emsp;

- (為了優化搜尋效能，所以有補加 username 的 INDEX)

![](images/Q3-5-1.png)
&emsp;

### 6.使用 SELECT 指令取得欄位 username 是 test 且欄位 password 也是 test 的資料。

![](images/Q3-6.png)
&emsp;

### 7.使用 UPDATE 指令更新欄位 username 是 test 的會員資料，將資料中的 name 欄位改成 test2。

![](images/Q3-7.png)
&emsp;

---

## 要求四

### 1.取得 member 資料表中，總共有幾筆資料 ( 幾位會員 )。

![](images/Q4-1.png)
&emsp;

### 2.取得 member 資料表中，所有會員 follower_count 欄位的總和。

![](images/Q4-2.png)
&emsp;

### 3.取得 member 資料表中，所有會員 follower_count 欄位的平均數。

![](images/Q4-3.png)
&emsp;

---

## 要求五

### 1.建立 message 資料表**

![](images/Q5-1.png)
&emsp;

- 使用 INSERT 指令將資料新增至 message 資料表中。

![](images/Q5-1-1.png)
&emsp;


### 2.使用 SELECT 搭配 JOIN 語法，取得所有留言，結果須包含留言者會員的姓名。

![](images/Q5-2.png)
&emsp;

### 3.使用 SELECT 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留言，資料中須包含留言者會員的姓名。

![](images/Q5-3.png)
&emsp;

### 4.使用 SELECT、SQL Aggregate Functions 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留言平均按讚數。

![](images/Q5-4.png)
&emsp;

### 使用 mysqldump 匯出資料

![](images/mysqldump.png)