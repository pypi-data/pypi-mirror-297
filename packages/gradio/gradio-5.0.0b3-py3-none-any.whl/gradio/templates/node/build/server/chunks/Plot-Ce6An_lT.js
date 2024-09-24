import { c as create_ssr_component, v as validate_component, m as missing_component } from './ssr-Cz1f32Mr.js';
import './2-DleTh3G7.js';
import { E as Empty } from './Empty-CAGwpzL4.js';
import './index4-D_FyJKAV.js';

const Plot$2 = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--carbon" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><circle cx="20" cy="4" r="2" fill="currentColor"></circle><circle cx="8" cy="16" r="2" fill="currentColor"></circle><circle cx="28" cy="12" r="2" fill="currentColor"></circle><circle cx="11" cy="7" r="2" fill="currentColor"></circle><circle cx="16" cy="24" r="2" fill="currentColor"></circle><path fill="currentColor" d="M30 3.413L28.586 2L4 26.585V2H2v26a2 2 0 0 0 2 2h26v-2H5.413Z"></path></svg>`;
});
const Plot = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value } = $$props;
  let { target } = $$props;
  let { colors = [] } = $$props;
  let { theme_mode } = $$props;
  let { caption } = $$props;
  let { bokeh_version } = $$props;
  let { show_actions_button } = $$props;
  let { gradio } = $$props;
  let { x_lim = null } = $$props;
  let { _selectable } = $$props;
  let PlotComponent = null;
  let _type = value?.type;
  const plotTypeMapping = {
    plotly: () => import('./PlotlyPlot-BCAN8zg5.js'),
    bokeh: () => import('./BokehPlot-BpzCy0Vt.js'),
    altair: () => import('./AltairPlot-uPetx01k.js'),
    matplotlib: () => import('./MatplotlibPlot-DqzpX6T_.js')
  };
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.target === void 0 && $$bindings.target && target !== void 0)
    $$bindings.target(target);
  if ($$props.colors === void 0 && $$bindings.colors && colors !== void 0)
    $$bindings.colors(colors);
  if ($$props.theme_mode === void 0 && $$bindings.theme_mode && theme_mode !== void 0)
    $$bindings.theme_mode(theme_mode);
  if ($$props.caption === void 0 && $$bindings.caption && caption !== void 0)
    $$bindings.caption(caption);
  if ($$props.bokeh_version === void 0 && $$bindings.bokeh_version && bokeh_version !== void 0)
    $$bindings.bokeh_version(bokeh_version);
  if ($$props.show_actions_button === void 0 && $$bindings.show_actions_button && show_actions_button !== void 0)
    $$bindings.show_actions_button(show_actions_button);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  if ($$props.x_lim === void 0 && $$bindings.x_lim && x_lim !== void 0)
    $$bindings.x_lim(x_lim);
  if ($$props._selectable === void 0 && $$bindings._selectable && _selectable !== void 0)
    $$bindings._selectable(_selectable);
  {
    {
      let type = value?.type;
      if (type !== _type) {
        PlotComponent = null;
      }
      if (type && type in plotTypeMapping) {
        plotTypeMapping[type]().then((module) => {
          PlotComponent = module.default;
        });
      }
    }
  }
  return `${value && PlotComponent ? `${validate_component(PlotComponent || missing_component, "svelte:component").$$render(
    $$result,
    {
      value,
      target,
      colors,
      theme_mode,
      caption,
      bokeh_version,
      show_actions_button,
      gradio,
      _selectable,
      x_lim
    },
    {},
    {}
  )}` : `${validate_component(Empty, "Empty").$$render($$result, { unpadded_box: true, size: "large" }, {}, {
    default: () => {
      return `${validate_component(Plot$2, "PlotIcon").$$render($$result, {}, {}, {})}`;
    }
  })}`}`;
});
const Plot$1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: Plot
}, Symbol.toStringTag, { value: "Module" }));

export { Plot$2 as P, Plot as a, Plot$1 as b };
//# sourceMappingURL=Plot-Ce6An_lT.js.map
