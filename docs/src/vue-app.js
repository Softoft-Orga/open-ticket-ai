import { createApp, createSSRApp, h } from 'vue';

// Astro calls this with (App, props, { head })
export default (App, props) => {
  const create = import.meta.env.SSR ? createSSRApp : createApp;
  const app = create({ render: () => h(App, props) });
  return { app };
};
