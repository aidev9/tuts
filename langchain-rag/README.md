## Tasks

### Install Docker Desktop

- Navigate to https://www.docker.com/products/docker-desktop
- Click Download Docker Desktop - choose your OS and chip version
- While downloading, create a free account with Docker. You'll need it later.
- Once downloaded, follow the setup instructions, sign in with your account and verify Docker Desktop is running by clicking the whale icon on MacOS

### Install Supabase

- `brew install supabase/tap/supabase`
- `cd dev_folder`
- `supabase init`
- `supabase start`
  - This will take a few minutes, as images will be downloaded
  - Monitor progress in the Docker Desktop interface
- Copy your development setup details and store them in a safe place, we'll need them later in the app. Items below are for illustration only:

```
         API URL: http://127.0.0.1:54321
     GraphQL URL: http://127.0.0.1:54321/graphql/v1
  S3 Storage URL: http://127.0.0.1:54321/storage/v1/s3
          DB URL: postgresql://postgres:postgres@127.0.0.1:54322/postgres
      Studio URL: http://127.0.0.1:54323
    Inbucket URL: http://127.0.0.1:54324
      JWT secret: super-secret-jwt-token-with-at-least-32-characters-long
        anon key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU
   S3 Access Key: 625729a08b95bf1b7ff351a663f3a23c
   S3 Secret Key: 850181e4652dd023b7a98c58ae0d2d34bd487ee0cc3254aed6eda37307425907
       S3 Region: local
```

- Navigate to [http://localhost:54323](http://localhost:54323)

### Configure the vector table and functions

- Enable the pgvector extension

  - Go to the Database page in the Dashboard.
  - Click on Extensions in the sidebar.
  - Search for "vector" and enable the extension.

- Create a documents table in the public schema

```-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store your documents
create table
  documents (
    id uuid primary key,
    content text, -- corresponds to Document.pageContent
    metadata jsonb, -- corresponds to Document.metadata
    embedding vector (1536) -- 1536 works for OpenAI embeddings, change if needed
  );

-- Create a function to search for documents
create function match_documents (
  query_embedding vector (1536),
  filter jsonb default '{}'
) returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
) language plpgsql as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding;
end;
$$;
```

- Create a match_documents function in your database
- Install the supabase-py package

### Ingest a folder of architectural documents

- Recursive folder search
- Update Supabase index as new docs get added

### Ingest a GitHub repo
