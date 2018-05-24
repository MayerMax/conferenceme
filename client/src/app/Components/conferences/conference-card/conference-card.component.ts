import {Component, Input, OnInit} from '@angular/core';
import {Conference} from "../../../constructor/models/Conference";
import {ActivatedRoute, Router} from "@angular/router";
import {MatDialog} from "@angular/material";

@Component({
  selector: 'app-conference-card',
  templateUrl: './conference-card.component.html',
  styleUrls: ['./conference-card.component.css']
})
export class ConferenceCardComponent implements OnInit {
  @Input() conference: Conference;
  constructor(private  route: ActivatedRoute, private router: Router, public dialog: MatDialog) {

  }

  navigate(id: number) {
    this.router.navigate([{outlets: {primary: `constructor/conference/${id}`,sidemenu: 'constructor' }}]);
  }
  ngOnInit() {
  }

}
