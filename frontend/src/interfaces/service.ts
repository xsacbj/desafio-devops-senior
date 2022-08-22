export interface Service {
  id: number;
  description: string;
  time: number;
  status: string;
}

export interface ServiceElementProps{
  service: Service;
}
