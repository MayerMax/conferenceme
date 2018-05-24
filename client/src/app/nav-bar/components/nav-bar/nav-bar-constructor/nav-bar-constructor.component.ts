import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {MenuItem} from "../../../models/MenuItem";
import {StoreService} from "../../../../services/store.service";
@Component({
  selector: 'app-nav-bar-constructor',
  templateUrl: './nav-bar-constructor.component.html',
  styleUrls: ['./nav-bar-constructor.component.css']
})
export class NavBarConstructorComponent implements OnInit {

  menuItemsConstructor: Array<MenuItem> = null;
  idConference: number;
  loading;
  constructor(private  router: Router, private  activeRouter: ActivatedRoute,private storeService: StoreService) {
//     this.activeRouter.params.subscribe( val=> this.idConference = parseInt(val.id));
// console.log(this.idConference);
//     this.menuItemsConstructor = [
//       new MenuItem('', 'undo', this.activeRouter.snapshot.url.toString(), 'home'),
//       new MenuItem('Спикеры', 'account_circle', `constructor/conference/${ this.idConference}/speakers`,`constructor/${this.idConference}`),
//       new MenuItem('Лекции', 'school', `constructor/conference/${ this.idConference}/lectures`, `constructor/${this.idConference}`),
//       new MenuItem('Секции', 'store', `constructor/conference/${ this.idConference}/sections`, `constructor/${this.idConference}`),
//     ];
      }
  navigate(path: MenuItem) {
    if (path.icon === 'undo') {
      this.activeRouter.url.subscribe(
        (data) => {
          console.log(data);
          this.router.navigate([{outlets: { sidemenu: path.menuLink}}]);
        }
      ); }
    else {
      this.router.navigate([{outlets: {primary: path.link, sidemenu: path.menuLink}}]);
    }

  }
  ngOnInit() {
    setTimeout(() => this.storeService.ConferenceSubject$.subscribe(
      data => {
        if (data != null) {
          this.menuItemsConstructor = [
            new MenuItem('', 'undo', this.activeRouter.snapshot.url.toString(), 'home'),
            new MenuItem('Конференция', 'store', `constructor/conference/${  data.id}`, `constructor`),
            new MenuItem('Спикеры', 'account_circle', `constructor/conference/${ data.id}/speakers`, `constructor`),
            new MenuItem('Лекции', 'school', `constructor/conference/${  data.id}/lectures`, `constructor`),
            // new MenuItem('Секции', 'store', `constructor/conference/${  data.id}/sections`, `constructor`),
          ];
          this.loading = false;
        } else {
          this.menuItemsConstructor = [
            new MenuItem('', 'undo', this.activeRouter.snapshot.url.toString(), 'home')]
        }
      }
    ));
  }


}
