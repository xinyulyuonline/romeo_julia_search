# RomeoGPT

## Overview

RomeoGPT is a FastAPI-based question-answering system built around Shakespeare's *Romeo and Juliet*.

The project uses a version of the book that has already been divided into 90 text chunks. Each chunk is converted into an embedding using Azure OpenAI and stored for semantic search.

When a user asks a question, the system:

1. Converts the question into an embedding.
2. Compares it to the stored chunk embeddings.
3. Finds the most relevant text passages.
4. Sends the retrieved context to an Azure OpenAI language model.
5. Returns an answer based on the content of the book.

## Features

* FastAPI REST API
* Azure OpenAI embeddings
* Semantic search using vector similarity
* Question answering based on *Romeo and Juliet*
* Retrieval-Augmented Generation (RAG)

## Technologies

* Python
* FastAPI
* Azure OpenAI

## Project Goal

The goal of RomeoGPT is to demonstrate how embeddings and semantic search can be used to build a question-answering system for literary texts.
