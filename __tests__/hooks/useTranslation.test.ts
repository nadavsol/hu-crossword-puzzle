import { renderHook } from "@testing-library/react";
import { useTranslation } from "@/hooks/useTranslation";

describe("useTranslation", () => {
  test("returns Hungarian translation by default", () => {
    const { result } = renderHook(() => useTranslation("hu"));
    expect(result.current.t("app.title")).toBe("Keresztrejtvény");
  });

  test("returns Hebrew translation", () => {
    const { result } = renderHook(() => useTranslation("he"));
    expect(result.current.t("app.title")).toBe("תשבץ");
  });

  test("returns key when translation is missing", () => {
    const { result } = renderHook(() => useTranslation("hu"));
    expect(result.current.t("nonexistent.key")).toBe("nonexistent.key");
  });

  test("localizedString extracts correct language", () => {
    const { result } = renderHook(() => useTranslation("hu"));
    expect(
      result.current.ls({ hu: "Magyar", he: "הונגרית" })
    ).toBe("Magyar");
  });

  test("localizedString extracts Hebrew", () => {
    const { result } = renderHook(() => useTranslation("he"));
    expect(
      result.current.ls({ hu: "Magyar", he: "הונגרית" })
    ).toBe("הונגרית");
  });
});
