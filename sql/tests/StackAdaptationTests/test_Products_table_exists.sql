CREATE PROCEDURE StackAdaptationTests.[test Products table exists] -- noqa: CP02, RF05
AS
BEGIN
    IF OBJECT_ID(N'dbo.Products', N'U') IS NULL
        BEGIN
            EXEC tSQLt.Fail N'dbo.Products must exist as a real user table'; -- noqa: CP02
        END;
END;
GO
