#### 打印当前数据库名称
`SELECT DATABASE()`

#### 创建数据库
`CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name`

#### 撤销数据库
`DROP {DATABASE | SCHEMA} [IF EXISTS] db_name`

#### 创建表
```sql
CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name
    (create_definition,...)
    [table_options]
    [partition_options]
```

```sql
CREATE TABLE SC
    (
        SID CHAR(4) NOT NULL,
        CID CHAR(4) NOT NULL,
        SCORE SMALLINT,
        PRIMARY KEY(SID,CID),
        FOREIGN KEY(SID) REFERENCES S(SID),
        FOREIGN KEY(CID) REFERENCES C(CID)
    );
```

#### 删除表
```sql
DROP [TEMPORARY] TABLE [IF EXISTS]
    tbl_name [, tbl_name] ...
    [RESTRICT | CASCADE]
```

#### 更新表内容
```sql
UPDATE [LOW_PRIORITY] [IGNORE] table_reference
    SET col_name1={expr1|DEFAULT} [, col_name2={expr2|DEFAULT}] ...
    [WHERE where_condition]
    [ORDER BY ...]
    [LIMIT row_count]
```
Example:

```sql
UPDATE SC
SET SCORE=60
WHERE CID IN (SELECT CID FROM C WHERE CNAME='MATHS') AND SCORE <60;
```

`ERROR 1093 (HY000): You can't specify target table 't1' for update in FROM clause`

The error occurs when merging a derived table into the outer query block results in a statement
that both selects from and modifies a table. (Materialization does not cause the problem because,
in effect, it converts the derived table to a separate table.) To avoid this error, disable the
derived_merge flag of the optimizer_switch system variable before executing the statement:
`SET optimizer_switch = 'derived_merge=off';`

#### 增加列
```sql
ALTER TABLE tbl_name ADD
```

### 新建索引
```sql
CREATE [UNIQUE|FULLTEXT|SPATIAL] INDEX index_name
    [index_type]
    ON tbl_name (index_col_name,...)
    [index_option]
    [algorithm_option | lock_option] ...

index_col_name:
    col_name [(length)] [ASC | DESC]

index_type:
    USING {BTREE | HASH}

index_option:
      KEY_BLOCK_SIZE [=] value
    | index_type
    | WITH PARSER parser_name
    | COMMENT 'string'

algorithm_option:
    ALGORITHM [=] {DEFAULT|INPLACE|COPY}

lock_option:
    LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}
```

#### 删除索引
```sql
DROP INDEX index_name ON tbl_name
    [algorithm_option | lock_option] ...

algorithm_option:
    ALGORITHM [=] {DEFAULT|INPLACE|COPY}

lock_option:
    LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}
```
#### 修改表结构
##### 增加域：

```sql
ALTER TABLE tbl_name ADD [COLUMN] col_name column_definition [FIRST | AFTER col_name ]
||
ALTER TABLE tbl_name ADD [COLUMN] (col_name column_definition,...)

ALTER TABLE SC ADD semester_assessment char(100);
```
##### 删除域：

```sql
ALTER TABLE tbl_name DROP [COLUMN] col_name

ALTER TABLE SC DROP semester_assessment
```

##### 修改域
```sql
ALTER TABLE tbl_name MODIFY [COLUMN] col_name column_definition [FIRST | AFTER col_name]

ALTER TABLE S MODIFY SID CHAR(6);
```

