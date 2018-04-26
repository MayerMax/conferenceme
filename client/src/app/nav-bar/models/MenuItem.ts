export  class MenuItem {
  public name: string;
  public link: string;
  public icon: string;
  public menuLink: string;
  constructor(name, icon, link, menuLink) {
    this.name = name;
    this.icon = icon;
    this.link = link;
    this.menuLink = menuLink;
  }
}
