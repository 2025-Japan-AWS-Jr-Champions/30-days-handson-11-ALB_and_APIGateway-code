import {
  Question,
  AnswerRequest,
  AnswerResponse,
  RankingEntry,
} from "../types/quiz.js";

const API_BASE = "/api";

export async function fetchQuestions(username: string): Promise<Question[]> {
  const response = await fetch(
    `${API_BASE}/questions?username=${encodeURIComponent(username)}`,
  );
  if (!response.ok) {
    throw new Error("Failed to get questions");
  }
  return response.json();
}

export async function postAnswer(
  payload: AnswerRequest,
): Promise<AnswerResponse> {
  const response = await fetch(`${API_BASE}/answer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error("Failed to submit answer");
  }
  return response.json();
}

export async function fetchRanking(): Promise<RankingEntry[]> {
  const response = await fetch(`${API_BASE}/ranking`);
  if (!response.ok) {
    throw new Error("Failed to get ranking");
  }
  return response.json();
}
