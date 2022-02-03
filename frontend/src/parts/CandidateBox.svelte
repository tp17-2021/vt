<script>
    export let id;
    export let img;
    export let name;
    export let degree;
    export let age;
    export let profession;
    export let city;
</script>

<style lang="scss">
  .candidateBox {
    background: #dddddd;
    padding: 1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;

    &:hover {
      background: #999999;
    }

    .candidateBox-textInfo {
      .candidateBox-name {
        font-size: 24px;
        font-weight: bold;
      }

      > * {
        margin-bottom: .5rem;
        margin-left: 1rem;
      }

      .candidateBox-textDetail {
        display: flex;
        flex-direction: row;

        > * {
          margin-right: 1rem
        }
      }
    }

    img {
      border-radius: 100%;
      width: 100px;
      height: 100px;
      object-fit: cover;
      object-position: top center;
      margin-right: 2rem;
    }
  }
</style>
<div class="candidateBox">
<!--    <img src="{img}" alt="" height="50px">-->
    <div class="candidateBox-textInfo">
        <div class="candidateBox-name">{id}. {name}</div>
        <div class="candidateBox-textDetail">
            <div>{degree}</div>
            <div>{age} rokov</div>
            <div>{profession}</div>
            <div>{city}</div>
        </div>
    </div>
</div>