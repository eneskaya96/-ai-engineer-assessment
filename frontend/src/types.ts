export interface Address {
  id: number;
  address: string;
  matched_address: string;
  match_score: number;
}

export interface PaginatedAddresses {
  items: Address[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}
