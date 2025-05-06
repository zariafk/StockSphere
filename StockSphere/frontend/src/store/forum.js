import { defineStore } from 'pinia';

export const useForumStore = defineStore('forum', {
  state: () => ({
    communities: [],
    posts: [],
  }),
  actions: {
    // Fetching existing communities
    async fetchCommunities() {
      const response = await fetch('/api/communities/');
      this.communities = await response.json();
    },
    
    // Fetching existing posts associated with existing communits, repectively
    async fetchPosts(communityId) {
      const response = await fetch(`/api/posts/?community=${communityId}`);
      this.posts = await response.json();
    },
  },
});
