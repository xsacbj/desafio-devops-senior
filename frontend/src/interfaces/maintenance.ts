import { Service } from "./service";

export interface Maintenance {
  id: number;
  licensePlate: string;
  timeEstimate: number;
  status: string;
  createAt: string;
  services?: Service[];
}

export interface MaintenanceElementProps{
  maintenance: Maintenance;
}
