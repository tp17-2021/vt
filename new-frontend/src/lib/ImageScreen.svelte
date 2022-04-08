<script context="module" lang="ts">
    export enum icons {
        INSERT_TOKEN = "insert",
        SPINNER = "spinner",
        SUCCESS = "success",
        ERROR = "error",
        USB = "usb",
        NONE = "none",
    }
    // TODO: change usb position

</script>

<style lang="scss">
  .imageScreen {
    display: flex;
    flex-direction: column;
    align-items: center;

    img {
      margin-top: 3rem;
      margin-bottom: 1rem;
      width: 50%;
      height: auto;
    }

    .title {
      font-size: 1.5rem;
      margin-bottom: 3rem;
    }
  }
</style>

<script lang="ts">
    import {url} from "@roxi/routify";

    export let icon: icons = icons.SUCCESS
    export let title = ""
</script>


<div class="imageScreen">
    <img src={$url(`/img/icons/${icon}.png`)} alt="">
    <div class="title">{title}</div>
    <slot></slot>
</div>