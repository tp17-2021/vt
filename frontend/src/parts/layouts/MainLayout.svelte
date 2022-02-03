<script>
    import Header from "../Header.svelte";
</script>

<style type="text/scss">
  main {
    height: 100vh;

    .title {
      text-align: center;
      font-size: 2rem;
      font-weight: bold;
      padding: 1rem 1rem;
    }

    .subtitle {
      text-align: center;
      font-size: 1.5rem;
      font-weight: bold;
      padding: 1rem 1rem;
    }

    .content {
      padding: 1rem 2rem;
    }
  }
</style>

<main>
    <Header/>
    {#if $$slots.title}
        <div class="title">
            <slot name="title"/>
        </div>
    {/if}
    {#if $$slots.subtitle}
        <div class="subtitle">
            <slot name="subtitle"/>
        </div>
    {/if}
    <div class="content">
        <slot/>
    </div>
</main>
