<script>
  import { Router } from "@roxi/routify";
  import { routes } from "../.routify/routes";
  import './api/websocket';
  import {loadConfig} from "./api/rest";

  const config = {
      urlTransform: {
          // set base url based on environment variable
          apply: (url) => `${import.meta.env.VITE_BASE_PATH}${url}`, //external URL
          remove: (url) => url.replace(`${import.meta.env.VITE_BASE_PATH}`, '') //internal URL
      }
  };

  loadConfig();
</script>

<Router {routes} {config} />
