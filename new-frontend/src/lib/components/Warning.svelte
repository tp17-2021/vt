<script>
    export let text = "";
</script>

<style lang="scss">
  div {
    background-color: var(--yellow);
    padding: 1rem;
    margin: .5rem 0;
  }
</style>

<div>
    {text}<slot></slot>
</div>