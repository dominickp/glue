package client

type CatalogPageThread struct {
	Sub     string `json:"sub"`
	Com     string `json:"com"`
	Replies int    `json:"replies"`
}

type CatalogPage struct {
	PageNumber *int                `json:"page,omitempty"`
	Threads    []CatalogPageThread `json:"threads"`
}
