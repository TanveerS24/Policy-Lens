import { Pressable, Text, ViewStyle } from "react-native";

type Props = {
  label: string;
  onPress: () => void;
  disabled?: boolean;
  variant?: "primary" | "secondary" | "outline";
  style?: ViewStyle;
};

export default function Button({ label, onPress, disabled, variant = "primary", style }: Props) {
  const base =
    "rounded-xl px-6 py-3 shadow-soft items-center justify-center flex-row gap-2";

  const variants: Record<string, string> = {
    primary: "bg-primary",
    secondary: "bg-secondary",
    outline: "border border-slate-200 bg-white",
  };

  const textVariants: Record<string, string> = {
    primary: "text-white font-semibold",
    secondary: "text-white font-semibold",
    outline: "text-slate-700 font-semibold",
  };

  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      className={`${base} ${variants[variant]} ${disabled ? "opacity-40" : ""}`}
      style={style}
    >
      <Text className={textVariants[variant]}>{label}</Text>
    </Pressable>
  );
}
