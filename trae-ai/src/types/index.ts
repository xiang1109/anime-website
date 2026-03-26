export interface User {
  id: number;
  username: string;
  email: string;
  avatar?: string;
}

export interface Anime {
  id: number;
  title: string;
  description: string;
  cover_image: string;
  episodes: number;
  status: string;
  release_year: number;
  studio: string;
  average_rating: number;
  rating_count: number;
  created_at: string;
}

export interface Comment {
  id: number;
  user_id: number;
  anime_id: number;
  content: string;
  username: string;
  avatar?: string;
  created_at: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface RatingResponse {
  message: string;
  average_rating: number;
  rating_count: number;
  user_rating: number;
}
