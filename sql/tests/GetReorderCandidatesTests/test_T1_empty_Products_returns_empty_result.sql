CREATE PROCEDURE [GetReorderCandidatesTests].[test T1 empty Products returns empty result] -- noqa: RF05
AS
BEGIN
    SET NOCOUNT ON;
    EXEC [tSQLt].[FakeTable] @TableName = N'dbo.Products';

    CREATE TABLE #actual (
        [ProductID] INT,
        [ProductName] NVARCHAR(40),
        [Shortage] INT
    );
    CREATE TABLE #expected (
        [ProductID] INT,
        [ProductName] NVARCHAR(40),
        [Shortage] INT
    );

    INSERT INTO #actual ([ProductID], [ProductName], [Shortage])
    EXEC [dbo].[GetReorderCandidates];

    EXEC [tSQLt].[AssertEqualsTable] @Expected = N'#expected', @Actual = N'#actual';
END;
GO
