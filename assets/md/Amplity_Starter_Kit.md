# Amplity Chatbot

[Repository](https://github.com/ThoughtMinds/amplity-chatbot)

## Overview:

Local development happens inside Docker. This lets Azure service equivalents like Azurite be run locally.

There are a bunch of docker commands inside the [`Makefile`](https://github.com/ThoughtMinds/amplity-chatbot/blob/main/Makefile), you can go through them as you wish

In general you would make use of the following commands

### 1. Start services 

```
make devb
```

### 2. Shutodown 

```
make down
```

### 3. Get JWT Token for Authentication

```
make token
```

## Requirements

You will be needing a Pinecone account for testing locally.
Create an [account](https://www.pinecone.io/), while creating an index set the embedding model to `text-embedding-3-small`

Create an account at [ngrok](https://ngrok.com/) and claim your static domain. This will be passed to Azure Pub Sub.
You will receive your own `AZURE_PUBSUB_TASK_HUB_NAME` and `AZURE_PUBSUB_CONVERSATION_HUB_NAME`

Expose your local api using this command

```
ngrok http --url=true-deeply-gazelle.ngrok-free.app 9000
```

Here `9000` is the port of our FastAPI application