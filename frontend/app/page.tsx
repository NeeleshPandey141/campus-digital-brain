"use client";

import { useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import { uploadPDF, askQuestion } from "@/services/api";



type Source = {
  document: string;
  page: number;
};


type Message = {
  id: number;
  question: string;
  answer: string;
  sources: Source[];
};


export default function Home() {

  const fileInputRef = useRef<HTMLInputElement>(null);

  const [file, setFile] = useState<File | null>(null);

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState<Message[]>([]);

  const [hasUploadedDocument, setHasUploadedDocument] =
    useState(false);

  const [isUploading, setIsUploading] = useState(false);

  const [isAsking, setIsAsking] = useState(false);

  const [uploadMessage, setUploadMessage] = useState("");

  const [errorMessage, setErrorMessage] = useState("");


  function handleFileChange(
    selectedFile: File | undefined
  ) {

    if (!selectedFile) return;

    if (
      selectedFile.type !== "application/pdf" &&
      !selectedFile.name.toLowerCase().endsWith(".pdf")
    ) {

      setErrorMessage(
        "Please select a valid PDF file."
      );

      setFile(null);

      return;
    }

    setFile(selectedFile);

    setUploadMessage("");

    setErrorMessage("");
  }


  async function handleUpload() {

    if (!file) {

      setErrorMessage(
        "Please select a PDF before uploading."
      );

      return;
    }

    setIsUploading(true);

    setErrorMessage("");

    setUploadMessage("");

    try {

      const result = await uploadPDF(file);

      setHasUploadedDocument(true);

      setUploadMessage(
        `Successfully uploaded ${result.filename} (${result.chunks} chunks created)`
      );

    } catch (error) {

      console.error(error);

      const message =
        error instanceof Error
          ? error.message
          : "Upload failed. Please try again.";

      setErrorMessage(message);

    } finally {

      setIsUploading(false);
    }
  }


  async function handleAsk() {

    // Require at least one uploaded document
    if (!hasUploadedDocument) {

      setErrorMessage(
        "Please upload a document before asking a question."
      );

      return;
    }

    const currentQuestion = question.trim();

    if (!currentQuestion) {

      setErrorMessage(
        "Please enter a question."
      );

      return;
    }

    setIsAsking(true);

    setErrorMessage("");

    // Clear input immediately
    setQuestion("");

    try {

      const result = await askQuestion(
        currentQuestion
      );

      const newMessage: Message = {

        id: Date.now(),

        question: currentQuestion,

        answer: result.answer,

        sources: result.sources || [],
      };

      setMessages(
        (previousMessages) => [

          ...previousMessages,

          newMessage,

        ]
      );

    } catch (error) {

      console.error(error);

      const message =
        error instanceof Error
          ? error.message
          : "";

      // Restore question if request fails
      setQuestion(currentQuestion);

      if (

        message.toLowerCase().includes(
          "quota"
        ) ||

        message.toLowerCase().includes(
          "resource_exhausted"
        )

      ) {

        setErrorMessage(
          "AI service quota is temporarily exhausted. Please try again later."
        );

      } else {

        setErrorMessage(
          message ||
          "Unable to get an AI response right now. Please try again later."
        );
      }

    } finally {

      setIsAsking(false);
    }
  }


  function handleKeyDown(
    event: React.KeyboardEvent<HTMLInputElement>
  ) {

    if (

      event.key === "Enter" &&

      !isAsking

    ) {

      handleAsk();
    }
  }


  return (

    <main className="min-h-screen bg-slate-50">

      {/* HEADER */}

      <header className="border-b bg-white">

        <div className="mx-auto flex max-w-6xl items-center gap-3 px-6 py-5">

          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600 text-xl">

            🧠

          </div>


          <div>

            <h1 className="text-xl font-bold text-slate-900">

              Campus Digital Brain

            </h1>


            <p className="text-sm text-slate-500">

              Your AI-powered university knowledge assistant

            </p>

          </div>

        </div>

      </header>


      <div className="mx-auto max-w-5xl px-6 py-10">


        {/* HERO */}

        <section className="mb-10 text-center">

          <h2 className="text-4xl font-bold tracking-tight text-slate-900">

            Ask your documents anything.

          </h2>


          <p className="mx-auto mt-3 max-w-2xl text-slate-500">

            Upload your university notes and use AI to quickly find answers
            from your study material.

          </p>

        </section>


        {/* UPLOAD SECTION */}

        <section className="rounded-2xl border bg-white p-6 shadow-sm">

          <div className="mb-6">

            <h2 className="text-xl font-bold text-slate-900">

              Upload Document

            </h2>


            <p className="mt-1 text-sm text-slate-500">

              Upload a PDF containing your notes or study material.

            </p>

          </div>


          {/* UPLOAD AREA */}

          <div

            onClick={() =>
              fileInputRef.current?.click()
            }

            className="cursor-pointer rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 p-10 text-center transition hover:border-blue-500 hover:bg-blue-50"

          >

            <div className="mb-3 text-4xl">

              📄

            </div>


            <h3 className="font-semibold text-slate-800">

              Click to upload your PDF

            </h3>


            <p className="mt-2 text-sm text-slate-500">

              Select your university notes or study material

            </p>


            <input

              ref={fileInputRef}

              type="file"

              accept=".pdf,application/pdf"

              className="hidden"

              onChange={(event) =>
                handleFileChange(
                  event.target.files?.[0]
                )
              }

            />

          </div>


          {/* SELECTED FILE */}

          {file && (

            <div className="mt-5 flex items-center justify-between rounded-xl border border-blue-200 bg-blue-50 p-4">

              <div className="flex items-center gap-3">

                <span className="text-2xl">

                  📄

                </span>


                <div>

                  <p className="font-medium text-slate-800">

                    {file.name}

                  </p>


                  <p className="text-sm text-slate-500">

                    {(file.size / 1024 / 1024).toFixed(2)} MB

                  </p>

                </div>

              </div>


              <button

                onClick={(event) => {

                  event.stopPropagation();

                  setFile(null);

                  setUploadMessage("");

                }}

                className="text-sm font-medium text-red-500 hover:text-red-700"

              >

                Remove

              </button>

            </div>

          )}


          {/* UPLOAD BUTTON */}

          <button

            onClick={handleUpload}

            disabled={!file || isUploading}

            className="mt-5 w-full rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"

          >

            {isUploading

              ? "Uploading and processing..."

              : "Upload PDF"}

          </button>


          {/* UPLOAD SUCCESS */}

          {uploadMessage && (

            <div className="mt-4 rounded-xl border border-green-200 bg-green-50 p-4 text-sm text-green-700">

              ✓ {uploadMessage}

            </div>

          )}

        </section>


        {/* CHAT SECTION */}

        <section className="mt-8 rounded-2xl border bg-white p-6 shadow-sm">

          <div className="mb-6">

            <h2 className="text-xl font-bold text-slate-900">

              Ask Your Documents

            </h2>


            <p className="mt-1 text-sm text-slate-500">

              Ask questions based on the PDFs you have uploaded.

            </p>

          </div>


          {/* NO DOCUMENT MESSAGE */}

          {!hasUploadedDocument && (

            <div className="mb-6 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-700">

              📄 Upload a document first to start asking questions.

            </div>

          )}


          {/* CHAT HISTORY */}

          {messages.length > 0 && (

            <div className="mb-8 space-y-6">

              {messages.map((message) => (

                <div

                  key={message.id}

                  className="space-y-4"

                >


                  {/* USER QUESTION */}

                  <div className="flex justify-end">

                    <div className="max-w-2xl rounded-2xl rounded-tr-sm bg-blue-600 px-5 py-4 text-white shadow-sm">

                      <p className="text-xs font-semibold uppercase tracking-wide text-blue-100">

                        You

                      </p>


                      <p className="mt-1">

                        {message.question}

                      </p>

                    </div>

                  </div>


                  {/* AI ANSWER */}

                  <div className="flex justify-start">

                    <div className="answer-card w-full">

                      <div className="answer-header">

                        <span className="answer-icon">

                          ✦

                        </span>


                        <div>

                          <p className="answer-label">

                            Campus Digital Brain

                          </p>


                          <h2>

                            Here’s what I found

                          </h2>

                        </div>

                      </div>


                      <div className="answer-content">
                        <ReactMarkdown>
                        {message.answer}
                        </ReactMarkdown>
                      </div>


                      {/* SOURCES */}

                      {message.sources.length > 0 && (

                        <div className="sources-section">

                          <h3>

                            Sources

                          </h3>


                          <div className="sources-list">

                            {message.sources.map(

                              (source, index) => (

                                <div

                                  key={`${source.document}-${source.page}-${index}`}

                                  className="source-item"

                                >

                                  <div className="source-icon">

                                    📄

                                  </div>


                                  <div>

                                    <p className="source-document">

                                      {source.document}

                                    </p>


                                    <p className="source-page">

                                      Page {source.page}

                                    </p>

                                  </div>

                                </div>

                              )

                            )}

                          </div>

                        </div>

                      )}

                    </div>

                  </div>

                </div>

              ))}

            </div>

          )}


          {/* THINKING */}

          {isAsking && (

            <div className="mb-6 flex justify-start">

              <div className="rounded-2xl rounded-tl-sm border bg-slate-50 px-5 py-4">

                <p className="text-sm font-medium text-slate-600">

                  🧠 Campus Digital Brain is thinking...

                </p>

              </div>

            </div>

          )}


          {/* QUESTION INPUT */}

          <div className="flex gap-3">

            <input

              type="text"

              placeholder={

                hasUploadedDocument

                  ? "Ask a question about your documents..."

                  : "Upload a document to start asking..."

              }

              value={question}

              onChange={(event) =>
                setQuestion(event.target.value)
              }

              onKeyDown={handleKeyDown}

              disabled={
                isAsking ||
                !hasUploadedDocument
              }

              className="flex-1 rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100"

            />


            <button

              onClick={handleAsk}

              disabled={

                isAsking ||

                !hasUploadedDocument ||

                !question.trim()

              }

              className="rounded-xl bg-slate-900 px-6 py-3 font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"

            >

              {isAsking

                ? "Thinking..."

                : "Ask AI"}

            </button>

          </div>


          <p className="mt-3 text-xs text-slate-400">

            Press Enter to send your question.

          </p>

        </section>


        {/* ERROR MESSAGE */}

        {errorMessage && (

          <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4">

            <div className="flex gap-3">

              <span>

                ⚠️

              </span>


              <div>

                <h3 className="font-semibold text-red-700">

                  Something went wrong

                </h3>


                <p className="mt-1 text-sm text-red-600">

                  {errorMessage}

                </p>

              </div>

            </div>

          </div>

        )}

      </div>

    </main>

  );
}