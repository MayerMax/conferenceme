import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {MenuItem} from "../../models/MenuItem";
@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent implements OnInit {
  menuItemsHome: Array<MenuItem> = [
    new MenuItem('home', 'home', 'home', 'home'),
    // new MenuItem('Новости', 'class', 'home', 'home'),
    new MenuItem('Наши конференции', 'watch_later', 'conferences', 'home'),
  ];
  // @Input() parentComponent: string;
  // parenthome = false;
  constructor(private router: Router, private  route: ActivatedRoute ) {
    // const url: Observable<string> =
    //   route.root;
  }

  navigate(path: MenuItem) {
    this.router.navigate([{outlets: {primary: path.link, sidemenu: path.menuLink }}]  );

  }
  ngOnInit() {
  }

}
