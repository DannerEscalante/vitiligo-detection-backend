export function formatAppointmentDateTime(value: string) {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return {
      date: "Fecha invalida",
      time: "--:--",
      label: "Fecha invalida"
    };
  }

  const formattedDate = new Intl.DateTimeFormat("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  }).format(date);

  const formattedTime = new Intl.DateTimeFormat("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  }).format(date);

  return {
    date: formattedDate,
    time: formattedTime,
    label: `${formattedDate} - ${formattedTime}`
  };
}
