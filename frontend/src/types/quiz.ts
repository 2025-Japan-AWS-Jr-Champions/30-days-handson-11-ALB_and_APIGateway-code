export interface Question {
  question_id: string;
  image_svg: string;
  choices: string[];
}

export interface AnswerRequest {
  username: string;
  questions: { quiz_id: string; answer: string }[];
}

export interface AnswerResponse {
  correct: number;
}

export interface RankingEntry {
  username: string;
  correct: number;
}
