// iRacing GT3 cars with parameter schemas
// Parameter schema defines what's adjustable per car for the structured form

const gt3ParameterSchema = {
  // ---- Tires ----
  tire_pressure_lf: { type: "float", label: "Tire Pressure LF", category: "tires", unit: "psi", min: 18.0, max: 30.0, step: 0.1 },
  tire_pressure_rf: { type: "float", label: "Tire Pressure RF", category: "tires", unit: "psi", min: 18.0, max: 30.0, step: 0.1 },
  tire_pressure_lr: { type: "float", label: "Tire Pressure LR", category: "tires", unit: "psi", min: 18.0, max: 30.0, step: 0.1 },
  tire_pressure_rr: { type: "float", label: "Tire Pressure RR", category: "tires", unit: "psi", min: 18.0, max: 30.0, step: 0.1 },

  // ---- Suspension: Camber ----
  camber_lf: { type: "float", label: "Camber LF", category: "suspension", unit: "deg", min: -5.0, max: 0.0, step: 0.1 },
  camber_rf: { type: "float", label: "Camber RF", category: "suspension", unit: "deg", min: -5.0, max: 0.0, step: 0.1 },
  camber_lr: { type: "float", label: "Camber LR", category: "suspension", unit: "deg", min: -4.0, max: 0.0, step: 0.1 },
  camber_rr: { type: "float", label: "Camber RR", category: "suspension", unit: "deg", min: -4.0, max: 0.0, step: 0.1 },

  // ---- Suspension: Toe ----
  toe_front: { type: "float", label: "Toe Front", category: "suspension", unit: "deg", min: -0.5, max: 0.5, step: 0.01 },
  toe_rear: { type: "float", label: "Toe Rear", category: "suspension", unit: "deg", min: -0.3, max: 0.5, step: 0.01 },

  // ---- Suspension: Springs ----
  spring_rate_lf: { type: "integer", label: "Spring Rate LF", category: "suspension", unit: "N/mm", min: 50, max: 300, step: 5 },
  spring_rate_rf: { type: "integer", label: "Spring Rate RF", category: "suspension", unit: "N/mm", min: 50, max: 300, step: 5 },
  spring_rate_lr: { type: "integer", label: "Spring Rate LR", category: "suspension", unit: "N/mm", min: 50, max: 300, step: 5 },
  spring_rate_rr: { type: "integer", label: "Spring Rate RR", category: "suspension", unit: "N/mm", min: 50, max: 300, step: 5 },

  // ---- Suspension: Ride Height ----
  ride_height_front: { type: "float", label: "Ride Height Front", category: "suspension", unit: "mm", min: 40, max: 100, step: 0.5 },
  ride_height_rear: { type: "float", label: "Ride Height Rear", category: "suspension", unit: "mm", min: 50, max: 120, step: 0.5 },

  // ---- Suspension: Anti-Roll Bars ----
  arb_front: { type: "discrete", label: "ARB Front", category: "suspension", values: ["D1", "D2", "D3", "D4", "D5", "D6"] },
  arb_rear: { type: "discrete", label: "ARB Rear", category: "suspension", values: ["D1", "D2", "D3", "D4", "D5", "D6"] },

  // ---- Suspension: Dampers ----
  damper_lf_bump_slow: { type: "integer", label: "Damper LF Bump (Slow)", category: "suspension", min: 0, max: 12, step: 1 },
  damper_lf_rebound_slow: { type: "integer", label: "Damper LF Rebound (Slow)", category: "suspension", min: 0, max: 12, step: 1 },
  damper_rf_bump_slow: { type: "integer", label: "Damper RF Bump (Slow)", category: "suspension", min: 0, max: 12, step: 1 },
  damper_rf_rebound_slow: { type: "integer", label: "Damper RF Rebound (Slow)", category: "suspension", min: 0, max: 12, step: 1 },
  damper_lr_bump_slow: { type: "integer", label: "Damper LR Bump (Slow)", category: "suspension", min: 0, max: 12, step: 1 },
  damper_lr_rebound_slow: { type: "integer", label: "Damper LR Rebound (Slow)", category: "suspension", min: 0, max: 12, step: 1 },
  damper_rr_bump_slow: { type: "integer", label: "Damper RR Bump (Slow)", category: "suspension", min: 0, max: 12, step: 1 },
  damper_rr_rebound_slow: { type: "integer", label: "Damper RR Rebound (Slow)", category: "suspension", min: 0, max: 12, step: 1 },

  // ---- Aero ----
  front_splitter: { type: "integer", label: "Front Splitter", category: "aero", min: 0, max: 5, step: 1 },
  rear_wing: { type: "integer", label: "Rear Wing", category: "aero", min: 1, max: 10, step: 1 },

  // ---- Brakes ----
  brake_bias: { type: "float", label: "Brake Bias", category: "brakes", unit: "%", min: 44.0, max: 64.0, step: 0.1 },
  brake_pressure: { type: "integer", label: "Brake Pressure", category: "brakes", unit: "%", min: 50, max: 100, step: 1 },

  // ---- Electronics ----
  abs: { type: "integer", label: "ABS", category: "electronics", min: 0, max: 12, step: 1 },
  tc: { type: "integer", label: "Traction Control", category: "electronics", min: 0, max: 12, step: 1 },
  tc2: { type: "integer", label: "TC2 / TC Cut", category: "electronics", min: 0, max: 10, step: 1 },

  // ---- Differential ----
  diff_preload: { type: "integer", label: "Diff Preload", category: "differential", min: 0, max: 10, step: 1 },
  diff_power_ramp: { type: "integer", label: "Diff Power Ramp", category: "differential", min: 20, max: 90, step: 5 },
  diff_coast_ramp: { type: "integer", label: "Diff Coast Ramp", category: "differential", min: 20, max: 90, step: 5 },

  // ---- Fuel ----
  fuel_load: { type: "integer", label: "Fuel Load", category: "fuel", unit: "L", min: 0, max: 120, step: 1 },
};

export const iRacingCars = [
  {
    sim: "iracing" as const,
    name: "BMW M4 GT3",
    manufacturer: "BMW",
    carClass: "gt3" as const,
    parameterSchema: gt3ParameterSchema,
    metadata: { year: 2022, power_hp: 590, weight_kg: 1310 },
  },
  {
    sim: "iracing" as const,
    name: "Ferrari 296 GT3",
    manufacturer: "Ferrari",
    carClass: "gt3" as const,
    parameterSchema: gt3ParameterSchema,
    metadata: { year: 2023, power_hp: 600, weight_kg: 1290 },
  },
  {
    sim: "iracing" as const,
    name: "Porsche 911 GT3 R (992)",
    manufacturer: "Porsche",
    carClass: "gt3" as const,
    parameterSchema: gt3ParameterSchema,
    metadata: { year: 2023, power_hp: 565, weight_kg: 1300 },
  },
  {
    sim: "iracing" as const,
    name: "Mercedes-AMG GT3 2020",
    manufacturer: "Mercedes-AMG",
    carClass: "gt3" as const,
    parameterSchema: gt3ParameterSchema,
    metadata: { year: 2020, power_hp: 550, weight_kg: 1285 },
  },
  {
    sim: "iracing" as const,
    name: "Audi R8 LMS GT3 Evo II",
    manufacturer: "Audi",
    carClass: "gt3" as const,
    parameterSchema: gt3ParameterSchema,
    metadata: { year: 2022, power_hp: 585, weight_kg: 1310 },
  },
  {
    sim: "iracing" as const,
    name: "Lamborghini Huracan GT3 EVO",
    manufacturer: "Lamborghini",
    carClass: "gt3" as const,
    parameterSchema: gt3ParameterSchema,
    metadata: { year: 2022, power_hp: 580, weight_kg: 1300 },
  },
  {
    sim: "iracing" as const,
    name: "McLaren 720S GT3 Evo",
    manufacturer: "McLaren",
    carClass: "gt3" as const,
    parameterSchema: gt3ParameterSchema,
    metadata: { year: 2023, power_hp: 570, weight_kg: 1295 },
  },
  {
    sim: "iracing" as const,
    name: "Aston Martin Vantage GT3",
    manufacturer: "Aston Martin",
    carClass: "gt3" as const,
    parameterSchema: gt3ParameterSchema,
    metadata: { year: 2024, power_hp: 575, weight_kg: 1305 },
  },
];
