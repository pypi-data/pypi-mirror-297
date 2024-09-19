/**
 * @license
 * Cesium - https://github.com/CesiumGS/cesium
 * Version 1.121.1
 *
 * Copyright 2011-2022 Cesium Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Columbus View (Pat. Pend.)
 *
 * Portions licensed separately.
 * See https://github.com/CesiumGS/cesium/blob/main/LICENSE.md for full licensing details.
 */

import {
  PrimitivePipeline_default
} from "./chunk-TERIAG53.js";
import {
  createTaskProcessorWorker_default
} from "./chunk-2O7GKV5K.js";
import "./chunk-KWQYSZMJ.js";
import "./chunk-3XJWWJ6Z.js";
import "./chunk-A6S75LTQ.js";
import "./chunk-VMFZWGK2.js";
import "./chunk-PZ2MFNIK.js";
import "./chunk-ZGKUIMX6.js";
import "./chunk-X2SXJCAR.js";
import "./chunk-N5CPCPYJ.js";
import "./chunk-ER27H77Q.js";
import "./chunk-CFJUTZIR.js";
import "./chunk-EI7MWQAW.js";
import "./chunk-VE7G5YJZ.js";
import "./chunk-MYMBHBEC.js";
import "./chunk-BHECY3WQ.js";
import "./chunk-U6I2SEH5.js";
import "./chunk-RTLXYA3C.js";
import "./chunk-IO3GOLZO.js";
import "./chunk-UVBMNHAS.js";
import "./chunk-XHOG2TOH.js";

// packages/engine/Source/Workers/combineGeometry.js
function combineGeometry(packedParameters, transferableObjects) {
  const parameters = PrimitivePipeline_default.unpackCombineGeometryParameters(
    packedParameters
  );
  const results = PrimitivePipeline_default.combineGeometry(parameters);
  return PrimitivePipeline_default.packCombineGeometryResults(
    results,
    transferableObjects
  );
}
var combineGeometry_default = createTaskProcessorWorker_default(combineGeometry);
export {
  combineGeometry_default as default
};
