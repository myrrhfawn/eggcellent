export interface SiteSettings {
  hero_title: string;
  hero_subtitle: string;
  instagram_url: string;
  telegram_url: string;
  facebook_url: string;
  contact_phone: string;
  contact_email: string;
  base_lesson_price: number;
}

export interface Teacher {
  id: number;
  name: string;
  photo: string;
  english_level: string;
  experience: string;
  bio: string;
  order: number;
}

export interface Review {
  id: number;
  author_name: string;
  text: string;
  rating: number;
  order: number;
}

export interface Plan {
  id: number;
  title: string;
  lessons_count: number;
  price_per_lesson: number;
  total_price: number;
  is_speaking_club: boolean;
  features: string[];
  note: string;
  is_highlighted: boolean;
  discount_percent: number;
  order: number;
}

export interface Answer {
  id: number;
  text: string;
}

export interface Question {
  id: number;
  text: string;
  points: number;
  answers: Answer[];
}

export interface Level {
  id: number;
  code: string;
  title: string;
  description: string;
  min_score: number;
  max_score: number;
}

export interface SubmitResult {
  id: number;
  score: number;
  max_score: number;
  level: Level | null;
}
