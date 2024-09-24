import { c as create_ssr_component, e as escape } from './ssr-Cz1f32Mr.js';

const css = {
  code: "div.svelte-1vvnm05{width:var(--size-10);height:var(--size-10)}.table.svelte-1vvnm05{margin:0 auto}",
  map: `{"version":3,"file":"Example.svelte","sources":["Example.svelte"],"sourcesContent":["<script lang=\\"ts\\">export let value;\\nexport let type;\\nexport let selected = false;\\n<\/script>\\n\\n<div\\n\\tstyle=\\"background-color: {value ? value : 'black'}\\"\\n\\tclass:table={type === \\"table\\"}\\n\\tclass:gallery={type === \\"gallery\\"}\\n\\tclass:selected\\n/>\\n\\n<style>\\n\\tdiv {\\n\\t\\twidth: var(--size-10);\\n\\t\\theight: var(--size-10);\\n\\t}\\n\\t.table {\\n\\t\\tmargin: 0 auto;\\n\\t}\\n</style>\\n"],"names":[],"mappings":"AAaC,kBAAI,CACH,KAAK,CAAE,IAAI,SAAS,CAAC,CACrB,MAAM,CAAE,IAAI,SAAS,CACtB,CACA,qBAAO,CACN,MAAM,CAAE,CAAC,CAAC,IACX"}`
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
  return `<div style="${"background-color: " + escape(value ? value : "black", true)}" class="${[
    "svelte-1vvnm05",
    (type === "table" ? "table" : "") + " " + (type === "gallery" ? "gallery" : "") + " " + (selected ? "selected" : "")
  ].join(" ").trim()}"></div>`;
});

export { Example as default };
//# sourceMappingURL=Example11-B3hKMNEv.js.map
