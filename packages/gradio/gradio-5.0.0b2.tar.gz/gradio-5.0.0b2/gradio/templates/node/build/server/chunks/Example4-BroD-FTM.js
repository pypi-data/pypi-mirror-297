import { c as create_ssr_component, v as validate_component } from './ssr-Cz1f32Mr.js';
import { I as Image$1 } from './Image2-CIpzhHTx.js';
import './file-url-D-K40zdU.js';

/* empty css                                       */
const css = {
  code: ".container.svelte-1sgcyba img{width:100%;height:100%}.container.selected.svelte-1sgcyba{border-color:var(--border-color-accent)}.border.table.svelte-1sgcyba{border:2px solid var(--border-color-primary)}.container.table.svelte-1sgcyba{margin:0 auto;border-radius:var(--radius-lg);overflow:hidden;width:var(--size-20);height:var(--size-20);object-fit:cover}.container.gallery.svelte-1sgcyba{width:var(--size-20);max-width:var(--size-20);object-fit:cover}",
  map: '{"version":3,"file":"Example.svelte","sources":["Example.svelte"],"sourcesContent":["<script lang=\\"ts\\">import Image from \\"./shared/Image.svelte\\";\\nexport let value;\\nexport let type;\\nexport let selected = false;\\n<\/script>\\n\\n<div\\n\\tclass=\\"container\\"\\n\\tclass:table={type === \\"table\\"}\\n\\tclass:gallery={type === \\"gallery\\"}\\n\\tclass:selected\\n\\tclass:border={value}\\n>\\n\\t{#if value}\\n\\t\\t<Image src={value.url} alt=\\"\\" />\\n\\t{/if}\\n</div>\\n\\n<style>\\n\\t.container :global(img) {\\n\\t\\twidth: 100%;\\n\\t\\theight: 100%;\\n\\t}\\n\\n\\t.container.selected {\\n\\t\\tborder-color: var(--border-color-accent);\\n\\t}\\n\\t.border.table {\\n\\t\\tborder: 2px solid var(--border-color-primary);\\n\\t}\\n\\n\\t.container.table {\\n\\t\\tmargin: 0 auto;\\n\\t\\tborder-radius: var(--radius-lg);\\n\\t\\toverflow: hidden;\\n\\t\\twidth: var(--size-20);\\n\\t\\theight: var(--size-20);\\n\\t\\tobject-fit: cover;\\n\\t}\\n\\n\\t.container.gallery {\\n\\t\\twidth: var(--size-20);\\n\\t\\tmax-width: var(--size-20);\\n\\t\\tobject-fit: cover;\\n\\t}\\n</style>\\n"],"names":[],"mappings":"AAmBC,yBAAU,CAAS,GAAK,CACvB,KAAK,CAAE,IAAI,CACX,MAAM,CAAE,IACT,CAEA,UAAU,wBAAU,CACnB,YAAY,CAAE,IAAI,qBAAqB,CACxC,CACA,OAAO,qBAAO,CACb,MAAM,CAAE,GAAG,CAAC,KAAK,CAAC,IAAI,sBAAsB,CAC7C,CAEA,UAAU,qBAAO,CAChB,MAAM,CAAE,CAAC,CAAC,IAAI,CACd,aAAa,CAAE,IAAI,WAAW,CAAC,CAC/B,QAAQ,CAAE,MAAM,CAChB,KAAK,CAAE,IAAI,SAAS,CAAC,CACrB,MAAM,CAAE,IAAI,SAAS,CAAC,CACtB,UAAU,CAAE,KACb,CAEA,UAAU,uBAAS,CAClB,KAAK,CAAE,IAAI,SAAS,CAAC,CACrB,SAAS,CAAE,IAAI,SAAS,CAAC,CACzB,UAAU,CAAE,KACb"}'
};
const Example = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value } = $$props;
  let { type } = $$props;
  let { selected = false } = $$props;
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.type === void 0 && $$bindings.type && type !== void 0)
    $$bindings.type(type);
  if ($$props.selected === void 0 && $$bindings.selected && selected !== void 0)
    $$bindings.selected(selected);
  $$result.css.add(css);
  return `<div class="${[
    "container svelte-1sgcyba",
    (type === "table" ? "table" : "") + " " + (type === "gallery" ? "gallery" : "") + " " + (selected ? "selected" : "") + " " + (value ? "border" : "")
  ].join(" ").trim()}">${value ? `${validate_component(Image$1, "Image").$$render($$result, { src: value.url, alt: "" }, {}, {})}` : ``} </div>`;
});

export { Example as default };
//# sourceMappingURL=Example4-BroD-FTM.js.map
