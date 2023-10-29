<script>
  import Router from 'svelte-spa-router'
  // import Home from "./routes/Home.svelte"
  import UpscaleImg from "./routes/UpscaleImg.svelte";

  const routes = {
    '/': UpscaleImg
  }
</script>

<Router {routes}/>