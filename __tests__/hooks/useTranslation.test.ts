import { renderHook } from "@testing-library/react";
import { useTranslation } from "@/hooks/useTranslation";

describe("useTranslation", () => {
  test("returns Hungarian translation", () => {
    const { result } = renderHook(() => useTranslation());
    expect(result.current.t("app.title")).toBe("Keresztrejtvény");
  });

  test("returns key when translation is missing", () => {
    const { result } = renderHook(() => useTranslation());
    expect(result.current.t("nonexistent.key")).toBe("nonexistent.key");
  });

  test("localizedString extracts Hungarian", () => {
    const { result } = renderHook(() => useTranslation());
    expect(
      result.current.ls({ hu: "Magyar" })
    ).toBe("Magyar");
  });
});
