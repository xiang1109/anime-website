export interface Anime {
  id: number;
  title: string;
  title_jp?: string;
  description: string;
  cover_image: string;
  episodes: number;
  status: string;
  release_year: number;
  release_date?: string;
  studio: string;
  genre?: string;
  average_rating: number | string;
  rating_count: number;
  nationality: string;
  anime_type: string;
  is_movie: number | boolean;
  created_at: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  isAdmin: boolean;
  createdAt: string;
}

export interface Comment {
  id: number;
  user_id: number;
  anime_id: number;
  content: string;
  username: string;
  created_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

export interface PagedResponse<T> {
  data: T[];
  pagination: {
    currentPage: number;
    totalPages: number;
    total: number;
    size: number;
  };
}
