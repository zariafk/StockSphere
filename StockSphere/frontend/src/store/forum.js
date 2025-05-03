import { defineStore } from 'pinia';

export const useForumStore = defineStore('forum', {
  state: () => ({
    communities: [],
    posts: [],
  }),
  actions: {
    async fetchCommunities() {
      const response = await fetch('/api/communities/');
      this.communities = await response.json();
    },
    async fetchPosts(communityId) {
      const response = await fetch(`/api/posts/?community=${communityId}`);
      this.posts = await response.json();
    },
  },
});
