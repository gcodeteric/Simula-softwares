import type { SetupParser, ParseResult } from "../types.js";
import { computeFileHash, getExtension } from "../utils.js";

/**
 * iRacing .sto file parser (stub).
 *
 * The iRacing .sto format is proprietary binary — we cannot extract
 * parameters from it without reverse engineering. For MVP:
 *
 * 1. We store the raw .sto file in R2/filesystem for download/revert
 * 2. We compute a SHA-256 hash for dedup and integrity checking
 * 3. Parameters are entered manually by the user via structured form
 *
 * When a real binary parser is developed (or if iRacing provides an API),
 * this stub can be replaced with a full implementation.
 */
export class IracingStoParser implements SetupParser {
  readonly id = "iracing-sto";
  readonly name = "iRacing Setup (.sto)";
  readonly sim = "iracing";
  readonly supportedExtensions = [".sto"];

  supports(filename: string): boolean {
    return this.supportedExtensions.includes(getExtension(filename));
  }

  async parse(buffer: Buffer, filename: string): Promise<ParseResult> {
    const fileHash = computeFileHash(buffer);

    return {
      fileHash,
      parameters: {},
      parametersComplete: false,
      warnings: [
        "iRacing .sto files are binary/proprietary. Parameters must be entered manually.",
      ],
    };
  }
}
