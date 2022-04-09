USE [FCS]
GO

-- /****** Object:  Table [dbo].[RevisionFileInfo]    Script Date: 04/05/2022 12:30:40 ******/
-- SET ANSI_NULLS ON
-- GO

-- SET QUOTED_IDENTIFIER ON
-- GO

CREATE TABLE [dbo].[RevisionFileInfo](
	[id] [uniqueidentifier] NOT NULL,
	[revision] [nvarchar](50) NOT NULL,
	[filename] [nvarchar](255) NOT NULL,
	[extension] [nvarchar](10) NULL,
	[mode] [nvarchar](7) NULL,
	[path] [nvarchar](255) NULL,
	[patharchive] [nvarchar](255) NULL,
	[isArchive] [bit] NULL
) ON [PRIMARY]

GO


