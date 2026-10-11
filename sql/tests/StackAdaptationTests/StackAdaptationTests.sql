CREATE SCHEMA StackAdaptationTests; -- noqa: CP02
GO
EXEC sys.sp_addextendedproperty -- noqa: CP02
    @name = N'tSQLt.TestClass',
    @value = 1,
    @level0type = N'SCHEMA',
    @level0name = N'StackAdaptationTests';
GO
