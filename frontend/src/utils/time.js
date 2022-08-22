export function convertTimeHoursToExtension(time) {
  const days = Math.floor(time / 24);
  const hours = time % 24;
  return `${days} days and ${hours} hours`;
}

export function formatDateTime(d) {
  // formate data time to dd/mm/yyyy hh:mm
  const date = new Date(d);
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear();
  const hour = date.getHours().toString().padStart(2, '0');
  const minute = date.getMinutes().toString().padStart(2, '0');
  return `${day}/${month}/${year} ${hour}:${minute}`;
}