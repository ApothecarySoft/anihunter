mainQuery = """
query($status: [MediaStatus], $sort: [MediaSort], $tag: String, $page: Int) {
  Page(page: $page) {
    pageInfo {
      hasNextPage
    }
    media(status_in: $status, sort: $sort, tag: $tag) {
      id
      type
      title {
        english
        userPreferred
      }
    }
  }
}
"""
