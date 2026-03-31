export interface Anime {
  id: number;
  title: string;
  title_jp?: string;
  description: string;
  coverImage: string;
  episodes: number;
  status: string;
  releaseYear: number;
  studio: string;
  genre?: string;
  averageRating: number;
  ratingCount: number;
  nationality: string;
  animeType: string;
  isMovie: boolean;
  createdAt: string;
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
  userId: number;
  animeId: number;
  content: string;
  username: string;
  createdAt: string;
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
